from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
from datetime import datetime
import os

app = FastAPI()

# Modelo de datos
class UserData(BaseModel):
    nombre: str
    edad: int
    profesion: str

# Carpeta de almacenamiento de JSONs
storage_dir = "/home/mateo/OperatingSystems-Final/backup"
os.makedirs(storage_dir, exist_ok=True)

@app.post("/save")
async def save(user_data: UserData):
    # Definir el nombre del archivo
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{user_data.nombre}_{timestamp}.json"
    file_path = os.path.join(storage_dir, file_name)

    # Guardar los datos en un archivo JSON
    with open(file_path, "w") as f:
        json.dump(user_data.dict(), f)

    return {"message": "Datos guardados correctamente.", "file_name": file_name}
