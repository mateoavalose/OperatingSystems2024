import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import asyncpg
from asyncpg.exceptions import DataError, UniqueViolationError
from pydantic import BaseModel
from typing import List

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
	page: int
	limit: int

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
