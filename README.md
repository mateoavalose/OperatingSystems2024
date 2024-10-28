#  FastAPI Service Deployment in AWS

This guide provides a comprehensive walkthrough for deploying a FastAPI application on an Amazon EC2 instance. It covers setting up a PostgreSQL database with Docker, managing the application as a systemd service, and making it publicly accessible via an Elastic IP.

## Prerequisites
1. **FastAPI application** created and tested locally.
2. **Data** in `.csv` format to load into PostgreSQL.
3. **SQL script** to create tables and import the `.csv` data.

### Notes
- This example uses the `docker-compose.yaml` file, `.csv` file, and **FastAPI** app from this repository.

---

## Steps

### 1. Create an EC2 Instance on AWS
1. Go to the **EC2 Dashboard** in AWS Console.
2. Click **Launch Instance** and configure:
   - **AMI**: Select **Ubuntu Server 20.04 LTS**.
   - **Instance Type**: Use **t2.micro** for testing.
   - **Key Pair**: Choose or create a key pair (e.g., `ec2-so.pem`).
   - **Network Settings**: Allow SSH (port 22).
3. Click **Launch Instance**.

### 2. Connect to the EC2 Instance
Connect using SSH:
```bash
ssh -i "ec2-so.pem" ubuntu@<your-ec2-public-ip>
```
Or, use the **Connect** option in AWS Console.

### 3. Update System Packages
```bash
sudo apt update && sudo apt upgrade -y
```

### 4. Install Python and Pip
```bash
sudo apt install python3-pip -y
```

### 5. Install Miniconda (Optional) or Set Up Virtual Environment
Miniconda is optional for package management. Use Miniconda for convenience or set up a `venv` virtual environment. Global installation is also possible.

**Using Miniconda:**
1. Install and initialize Miniconda:
   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   ~/miniconda3/bin/conda init
   sudo reboot
   ```
2. After reconnecting via SSH, set up a virtual environment:
   ```bash
   conda create --name FastAPI python=3.8
   conda activate FastAPI
   ```
3. Install packages:
   ```bash
   pip install fastapi[all] asyncpg boto3 python-dotenv
   ```

**Without Miniconda:**
1. Set up `venv`:
   ```bash
   python3 -m venv FastAPI
   source FastAPI/bin/activate
   ```
2. Install packages:
   ```bash
   pip install fastapi[all] asyncpg boto3 python-dotenv
   ```

### 6. Clone the Repository
```bash
git clone https://github.com/mateoavalose/OperatingSystems2024
cd OperatingSystems2024
```

### 7. Configure Environment Variables
Create `.env`:
```bash
nano .env
```
Add:
```perl
DATABASE_URL=postgresql://user:password@localhost:5433/ClassicRock
```

### 8. Set Up Docker and PostgreSQL
Install Docker:
```bash
sudo snap install docker
sudo chmod 666 /var/run/docker.sock
```
Start containers:
```bash
docker-compose up -d
docker update --restart unless-stopped postgres-operatingSystems
docker ps
```

### 9. Prepare PostgreSQL Database
1. Enter PostgreSQL container and create a data directory:
   ```bash
   docker exec -it postgres-operatingSystems bash
   mkdir Data
   exit
   ```
2. Copy `.csv` file to the container:
   ```bash
   docker cp ./Data/UltimateClassicRock.csv postgres-operatingSystems:/Data/
   ```
3. Edit SQL script (`Data/UploadPostgres.sql`) to structure and load data, then run it:
   SQL script used in example:
   ```sql
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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
    
    COPY MusicTracks (Track, Artist, Album, Year, Duration, Time_Signature, Danceability, Energy, Key, Loudness, Mode, Speechiness, Acousticness, Instrumentalness, Liveness, Valence, Tempo, Popularity)
    FROM '/Data/UltimateClassicRock.csv'
    DELIMITER ','
    CSV HEADER;
    
    SELECT COUNT(*) FROM MusicTracks;
   ```
   When the SQL script is ready, run:
   ```bash
   docker cp ./Data/*.sql postgres-operatingSystems:/Data/
   docker exec -it postgres-operatingSystems bash
   psql -U user -d ClassicRock -f /Data/UploadPostgres.sql
   rm -rf Data/
   exit
   ```

### 10. Set Up FastAPI as a Systemd Service
1. Create service file:
   ```bash
   sudo nano /etc/systemd/system/OperatingSystems-FastAPI.service
   ```
2. Add the following:
   ```ini
   [Unit]
   Description=FastAPI Application
   After=network.target

   [Service]
   User=ubuntu
   Group=ubuntu
   WorkingDirectory=/home/ubuntu/OperatingSystems2024
   ExecStart=/home/ubuntu/miniconda3/envs/FastAPI/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```
3. Start and enable service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start OperatingSystems-FastAPI
   sudo systemctl enable OperatingSystems-FastAPI
   sudo reboot
   ```
4. Verify service status:
   ```bash
   sudo systemctl status OperatingSystems-FastAPI
   ```

### 11. Test Endpoints Locally
```bash
curl -X 'GET' "http://127.0.0.1:8000/" -H 'accept: application/json'
```
Expected response: `{"message": "Connected to the database"}`.

### 12. Expose the Application Publicly
#### A. Assign an Elastic IP
1. In **Elastic IPs** on AWS, allocate and associate a new Elastic IP with your EC2 instance.

#### B. Configure Security Group
Update the security group to allow inbound traffic on port 8000:
1. Navigate to **Security Groups** in AWS.
2. Edit **Inbound rules**:
   - Type: **Custom TCP**
   - Protocol: **TCP**
   - Port Range: **8000**
   - Source: **0.0.0.0/0** (public access).
3. Save changes.

### 13. Access the FastAPI Application
Use the public IP to access FastAPI:
```url
http://<your-elastic-ip>:8000/
```
For Swagger documentation:
```url
http://<your-elastic-ip>:8000/docs
```

--- 
