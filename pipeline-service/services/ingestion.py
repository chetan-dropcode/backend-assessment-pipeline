import requests
import dlt
import os
from sqlalchemy.orm import Session
from models.customer import Customer

@dlt.resource(name="customers", write_disposition="merge", primary_key="customer_id")
def fetch_customers_from_api():
    base_url = "http://mock-server:5000/api/customers"
    page = 1
    limit = 100
    
    while True:
        response = requests.get(f"{base_url}?page={page}&limit={limit}", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        customers = data.get("data", [])
        if not customers:
            break
            
        yield customers
        
        if page * limit >= data.get("total", 0):
            break
        page += 1

def fetch_and_ingest(db: Session):
    # Fetch DB connection string
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/customer_db")
    
    # FIX: Explicitly set destination to 'postgres' and pass credentials 
    # to prevent dlt from defaulting to a local DuckDB file.
    pipeline = dlt.pipeline(
        pipeline_name='customer_pipeline',
        destination='postgres', 
        dataset_name='public',
        credentials=database_url
    )
    
    # Run the pipeline
    pipeline.run(fetch_customers_from_api())
    
    # PROOF: Query the actual PostgreSQL database to return the true row count
    return db.query(Customer).count()