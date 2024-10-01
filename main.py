import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import asyncpg
from asyncpg.exceptions import DataError, UniqueViolationError
from pydantic import BaseModel, condecimal, conint
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
	total: int
	page: Optional[int]
	total_pages: Optional[int]
	data: List[Dataset]

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
	page: Optional[int] = Query(None, ge=1),  # Page number (optional)
	track: Optional[str] = None,  # Optional filter by track name
	artist: Optional[str] = None,  # Optional filter by artist's name
	year: Optional[int] = None  # Optional filter by year 
):
	# Fixed limit to 100 rows per page
	limit = 100
	# SQL Dynamic Query
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
	# Obtain total rows without pagination
	total_query = "SELECT COUNT(*) FROM musictracks"
	if filters:
		total_query += " WHERE " + " AND ".join(filters)
	try:
		total = await app.state.db.fetchval(total_query, *params)
		if total == 0:
			return ResponseModel(total=0, page=None, total_pages=None, data=[])
		# Calculate total pages
		total_pages = (total + limit - 1) // limit
		# If no page is filtered and there's more than 100 rows, default to the first page
		if page is None and total > limit:
			page = 1
		# Apply pagination only if there are more than 100 rows
		if page:
			offset = (page - 1) * limit
			query += f" LIMIT {limit} OFFSET {offset}"
		else:
			query += f" LIMIT {limit}"
		# Execute query with pagination
		rows = await app.state.db.fetch(query, *params)
		data = [Dataset(track=row['track'], artist=row['artist'], year=row['year'], duration=row['duration']) for row in rows]
		return ResponseModel(total=total, page=page, total_pages=total_pages, data=data)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

# Pydantic moddel to validate input
class TrackInput(BaseModel):
    track: str
    artist: str
    album: str
    year: int
    duration: str
    time_signature: int
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    popularity: int

# Response with the rows inserted
class InsertResponseModel(BaseModel):
    added_records: int
    total_records: int

# Endpoint to insert values into the database
@app.post("/tracks", response_model=InsertResponseModel)
async def ingest_tracks(tracks: List[TrackInput]):
    try:
        # SQL para insertar los datos en la tabla (excluyendo TrackID)
        insert_query = '''
            INSERT INTO musictracks (
                track, artist, album, year, duration, time_signature, danceability, energy,
                key, loudness, mode, speechiness, acousticness, instrumentalness, liveness,
                valence, tempo, popularity
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
        '''

        # Iniciar la transacción e iterar sobre cada track para agregarlo a la base de datos
        async with app.state.db.transaction():
            for track in tracks:
                await app.state.db.execute(insert_query,
                    track.track, track.artist, track.album, track.year, track.duration,
                    track.time_signature, track.danceability, track.energy, track.key,
                    track.loudness, track.mode, track.speechiness, track.acousticness,
                    track.instrumentalness, track.liveness, track.valence, track.tempo, track.popularity
                )
        
        # Obtener el total de registros en la tabla después de la inserción
        total_query = "SELECT COUNT(*) FROM musictracks"
        total_records = await app.state.db.fetchval(total_query)

        # Devolver el número de registros agregados y el total de registros en la base de datos
        return InsertResponseModel(added_records=len(tracks), total_records=total_records)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting records: {str(e)}")