import psycopg2
import csv

# Datos de conexión a PostgreSQL
conn = psycopg2.connect(
    port=5433,
    host="localhost",  # Cambia esto por la IP o hostname de tu servidor de PostgreSQL
    database="MusicTracks",  # Cambia esto por el nombre de tu base de datos
    user="user",  # Cambia esto por tu usuario de PostgreSQL
    password="password"  # Cambia esto por tu contraseña
)

# Crear un cursor
cur = conn.cursor()

# Crear tabla si no existe
create_table_query = '''
DROP TABLE IF EXISTS MusicTracks;

CREATE TABLE MusicTracks (
    TrackID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Track TEXT,
    Artist TEXT,
    Album TEXT,
    Year INT,
    Duration TEXT,
    Time_Signature INT,
    Danceability DECIMAL(5, 2),
    Energy DECIMAL(5, 2),
    Key INT,
    Loudness DECIMAL(5, 2),
    Mode INT,
    Speechiness DECIMAL(5, 2),
    Acousticness DECIMAL(5, 2),
    Instrumentalness DECIMAL(5, 2),
    Liveness DECIMAL(5, 2),
    Valence DECIMAL(5, 2),
    Tempo DECIMAL(6, 2),
    Popularity INT
);
'''

# Ejecutar el comando para crear la tabla
cur.execute(create_table_query)

# Crear la extensión UUID si no existe
cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

# Función para insertar datos desde CSV
def insert_data_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Saltar el encabezado
        for row in reader:
            cur.execute(
                '''
                INSERT INTO MusicTracks (
                    Track, Artist, Album, Year, Duration, Time_Signature, Danceability, Energy, Key, Loudness, Mode, Speechiness, Acousticness, Instrumentalness, Liveness, Valence, Tempo, Popularity
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                row
            )

# Ruta del archivo CSV
csv_file_path = '/home/santiago/Escritorio/SistemasOperativos/Taller3/OperatingSystems2024/Data/UltimateClassicRock.csv'  # Cambia esto por la ruta de tu archivo CSV

# Llamar a la función para cargar datos
insert_data_from_csv(csv_file_path)

# Confirmar cambios
conn.commit()

# Cerrar cursor y conexión
cur.close()
conn.close()

print("Datos insertados correctamente.")
