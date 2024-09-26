DROP TABLE MusicTRacks

CREATE TABLE MusicTracks (
	TrackID UUID PRIMARY KEY,
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

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SELECT * FROM pg_extension;

ALTER TABLE MusicTracks
ALTER COLUMN TrackID SET DEFAULT uuid_generate_v4();

COPY MusicTracks (Track, Artist, Album, Year, Duration, Time_Signature, Danceability, Energy, Key, Loudness, Mode, Speechiness, Acousticness, Instrumentalness, Liveness, Valence, Tempo, Popularity)
FROM '/data.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM MusicTracks