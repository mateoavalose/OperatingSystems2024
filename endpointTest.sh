#!/bin/bash

### Test database connection
echo "---------------------------------------------"
echo "Testing connection to the database"
curl -X 'GET' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json'

echo ""

### Test GET method
echo "---------------------------------------------"
echo "Testing GET method with dynamic query. Leave empty if filter is not needed"
# Prompt user for parameters
read -p "Enter page number: " page
read -p "Enter track name: " track
read -p "Enter artist name: " artist
read -p "Enter year: " year

# Construct the URL with parameters
url="http://127.0.0.1:8000/tracks?"

# Append parameters only if they are provided
if [[ -n "$page" ]]; then
    url+="page=$page&"
fi
if [[ -n "$track" ]]; then
    url+="track=$track&"
fi
if [[ -n "$artist" ]]; then
    url+="artist=$artist&"
fi
if [[ -n "$year" ]]; then
    url+="year=$year&"
fi

# Remove the trailing '&' if it exists
url=${url%&}

# Execute the curl command
curl -X 'GET' "$url" -H 'accept: application/json'

echo ""

### Test POST method
echo "---------------------------------------------"
echo "Testing POST method"
# Prompt user for input
read -p "Enter track name: " track
read -p "Enter artist name: " artist
read -p "Enter album name: " album
read -p "Enter year (integer): " year
read -p "Enter duration: " duration
read -p "Enter time signature (integer): " time_signature
read -p "Enter danceability (0.0 to 1.0): " danceability
read -p "Enter energy (0.0 to 1.0): " energy
read -p "Enter key (integer): " key
read -p "Enter loudness (decimal): " loudness
read -p "Enter mode (0 or 1): " mode
read -p "Enter speechiness (decimal): " speechiness
read -p "Enter acousticness (decimal): " acousticness
read -p "Enter instrumentalness (decimal): " instrumentalness
read -p "Enter liveness (decimal): " liveness
read -p "Enter valence (decimal): " valence
read -p "Enter tempo (decimal): " tempo
read -p "Enter popularity (integer): " popularity

# Construct the JSON payload
json_payload=$(cat <<EOF
[
  {
    "track": "$track",
    "artist": "$artist",
    "album": "$album",
    "year": $year,
    "duration": "$duration",
    "time_signature": $time_signature,
    "danceability": $danceability,
    "energy": $energy,
    "key": $key,
    "loudness": $loudness,
    "mode": $mode,
    "speechiness": $speechiness,
    "acousticness": $acousticness,
    "instrumentalness": $instrumentalness,
    "liveness": $liveness,
    "valence": $valence,
    "tempo": $tempo,
    "popularity": $popularity
  }
]
EOF
)

# Execute the curl command
curl -X 'POST' \
  'http://127.0.0.1:8000/tracks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "$json_payload"