#!/bin/bash

# Define el directorio y el bucket
storage_dir="/home/mateo/OperatingSystems-Final/backup"
bucket_name="mae-so-ueia-2024"

# Sube archivos JSON al bucket y luego los elimina
for file in "$storage_dir"/*.json; do
    if [ -f "$file" ]; then
        aws s3 cp "$file" s3://$bucket_name/
        rm "$file"
    fi
done

# Crontab command:
# 45 7 * * * bash /home/mateo/OperatingSystems-Final/backup-s3.sh