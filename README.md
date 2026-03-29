# Backend Developer Technical Assessment

This project implements a complete data pipeline using Flask, FastAPI, and PostgreSQL, containerized with Docker.

## Architecture
1. **Mock Server (Flask):** Serves paginated customer data from a JSON file on port 5000.
2. **Database (PostgreSQL):** Stores customer records on port 5432.
3. **Pipeline Service (FastAPI):** Ingests data from the Mock Server using the `dlt` library and serves it via REST endpoints on port 8000.

## Prerequisites
* Docker Desktop
* Git

## How to Run
1. Clone the repository and navigate to the root directory.
2. Build and start the services:
   ```bash
   docker-compose up --build -d
3. Test the endpoints:
* View Mock Data: curl http://localhost:5000/api/customers?page=1&limit=5
* Trigger Ingestion: curl -X POST http://localhost:8000/api/ingest
* View Ingested Data: curl http://localhost:8000/api/customers?page=1&limit=5