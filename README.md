# Operating Systems - FastAPI 

## Overview

This project is a FastAPI-based web service for querying and inserting data into a relational database. The project demonstrates the use of RESTful endpoints to interact with a dataset loaded into a database, implementing features like filtering, pagination, and data validation.

## How to Run the Project

### 1. Set up the Virtual Environment
```bash
source /path/to/your/venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
uvicorn main:app --reload
```

### 4. Enable Service on System Startup
```bash
sudo systemctl daemon-reload
sudo systemctl start OperatingSystems-FastAPI
sudo systemctl enable OperatingSystems-FastAPI
```

### 5. Test the API
Use the provided `endpointTest.sh` script to verify that the API is working as expected.

### 6. Public Access via NGROK
Start the NGROK service to make the API publicly accessible:
```bash
ngrok http 8000
```

## Repository Structure

- `main.py`: FastAPI application code.
- `requirements.txt`: List of project dependencies.
- `data_loading.sql`: Script to load the dataset into the database.
- `endpointTest.sh`: Bash script for testing the API.
- `OperatingSystems-FastAPI.service`: Systemd service file for auto-start on machine boot.
- `setup.sh`: Bash script for setting up the virtual environment and installing dependencies.

## Project Components

### 1. Dataset Selection
The dataset used must contain at least 1000 records and include fields such as numerical or date-based columns. Some recommended sources for datasets include:
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Datos Gov](https://www.datos.gov.co/browse?sortBy=newest)

### 2. Database Setup
The dataset is loaded into a relational database such as PostgreSQL, MySQL, or DuckDB. The script used for loading data is included in the repository under the `data_loading.sql` file.

### 3. Virtual Environment and Dependencies
A virtual environment is used to manage project dependencies, which are listed in `requirements.txt`. To install the dependencies, run:
```bash
bash setup.sh
```

### 4. FastAPI Endpoints

#### **GET Endpoint**
- Allows users to query data from the database.
- Supports filtering to avoid returning the entire table.
- Paginated responses with a maximum of 100 records per request. A mechanism to retrieve the next set of data is implemented.

#### **POST Endpoint**
- Allows the insertion of new data into the database.
- Implements Pydantic models for validation of incoming data.
- The response includes the number of records inserted and the total records in the database after insertion.

### 5. Error Handling
The API includes proper exception handling to return the correct HTTP status codes in case of errors (e.g., 400 Bad Request, 500 Internal Server Error).

### 6. Endpoint Testing
A bash script (`endpointTest.sh`) is provided for testing both the GET and POST endpoints. It verifies both successful and unsuccessful cases using `curl`.

### 7. Service Setup
A `.service` file is configured for the FastAPI application to run automatically on system startup. This is designed to work with systemd on a WSL environment.

### 8. NGROK Integration
NGROK is used to make the API accessible over the internet. The configuration for this is included in the repository, and a public URL is generated for easy testing and access.
