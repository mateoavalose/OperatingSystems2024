import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import asyncpg
from asyncpg.exceptions import DataError, UniqueViolationError
from pydantic import BaseModel
from typing import List, Optional

# Create the FastAPI application
app = FastAPI()

### Database connection from .env
# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL from the .env file
DATABASE_URL = os.getenv('DATABASE_URL')

# Función para obtener una conexión a la base de datos
async def get_connection():
	return await asyncpg.connect(DATABASE_URL)

# Startup and closedown events 
@app.on_event("startup")
async def startup_event():
	app.state.db = await get_connection()

@app.on_event("shutdown")
async def shutdown_event():
	await app.state.db.close()

# Dataset model
class Dataset(BaseModel):
	track: str
	artist: str
	year: int
	duration: str

# Response model
class ResponseModel(BaseModel):
    data: List[Dataset]
    total: int
    page: Optional[int]
    total_pages: Optional[int]

# Complete model
class Item(BaseModel):
	TrackID: str
	Track: str
	Artist: str
	Album: str
	Year: int
	Duration: str
	Time_Signature: int
	Danceability: float
	Energy: float
	Key: int
	Loudness: float
	Mode: int
	Speechiness: float
	Acousticness: float
	Instrumentalness: float
	Liveness: float
	Valence: float
	Tempo: float
	Popularity: int

# Query to test connection to the database
@app.get("/")
async def read_root():
	try:
	   rows = await app.state.db.fetch('''
		SELECT 1
		''')
	   return {"message": "Connected to the database"}
	except Exception as e:
		return {"message": "Failed to connect to the database", "error": str(e)}

# Endpoint for filtering and paginating the data
@app.get("/tracks", response_model=ResponseModel)
async def get_tracks(
    page: Optional[int] = Query(None, ge=1),  # Paginación: número de página (opcional)
    track: Optional[str] = None,  # Filtro opcional por nombre de pista
    artist: Optional[str] = None,  # Filtro opcional por artista
    year: Optional[int] = None  # Filtro opcional por año
):
    # Límite fijo de 100 registros por página
    limit = 100

    # Construir consulta SQL dinámica
    query = "SELECT track, artist, year, duration FROM musictracks"
    filters = []
    params = []

    if track:
        filters.append("track ILIKE $1")
        params.append(f"%{track}%")
    if artist:
        filters.append("artist ILIKE $" + str(len(params) + 1))
        params.append(f"%{artist}%")
    if year:
        filters.append("year = $" + str(len(params) + 1))
        params.append(year)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    # Obtener total de filas sin paginación
    total_query = "SELECT COUNT(*) FROM musictracks"
    if filters:
        total_query += " WHERE " + " AND ".join(filters)

    try:
        total = await app.state.db.fetchval(total_query, *params)

        if total == 0:
            return ResponseModel(data=[], total=0, page=None, total_pages=None)

        # Calcular número de páginas totales
        total_pages = (total + limit - 1) // limit

        # Si no se especifica la página y hay más de 100 registros, por defecto es la primera página
        if page is None and total > limit:
            page = 1

        # Aplicar paginación solo si hay más de 100 registros
        if page:
            offset = (page - 1) * limit
            query += f" LIMIT {limit} OFFSET {offset}"
        else:
            query += f" LIMIT {limit}"

        # Ejecutar consulta con paginación
        rows = await app.state.db.fetch(query, *params)

        data = [Dataset(track=row['track'], artist=row['artist'], year=row['year'], duration=row['duration']) for row in rows]

        return ResponseModel(data=data, total=total, page=page, total_pages=total_pages)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))