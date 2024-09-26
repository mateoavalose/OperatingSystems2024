import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

app = FastAPI()

### Database connection from .env
# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL from the .env file
DATABASE_URL = os.getenv('DATABASE_URL')

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    try:
        # Run a simple query to test the connection
        db.execute(text("SELECT 1"))
        return {"message": "Connected to the database"}
    except Exception as e:
        return {"message": "Failed to connect to the database", "error": str(e)}

class Item(BaseModel):
    TrackID: str = 'id',
    Track: str = 'track',
    Artist: str = 'track',
    Album: str = 'album',
    Year: int = 0000,
    Duration: str = 'duration',
    Time_Signature: int = 0,
    Danceability: float = 0.00,
    Energy: float = 0.00,
    Key: int = 0,
    Loudness: float = 0.00,
    Mode: int = 0,
    Speechiness: float = 0.00,
    Acousticness: float = 0.00,
    Instrumentalness: float = 0.00,
    Liveness: float = 0.00,
    Valence: float = 0.00,
    Tempo: float = 0.0,
    Popularity: int = 0

