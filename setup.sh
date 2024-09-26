#!/bin/bash

python3 -m venv Entorno_Programa

source Entorno_Programa/bin/activate

echo "Instalando las librerías desde requirements.txt..."
pip install -r requirements.txt

deactivate

# Para dar permisos de ejecución:
chmod +x setup.sh