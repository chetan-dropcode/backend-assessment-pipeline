from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
from models.customer import Customer
from services.ingestion import fetch_and_ingest

# Notice we removed Base.metadata.create_all(bind=engine)
# dlt will now handle creating the table with its preferred schema.

app = FastAPI()

@app.post("/api/ingest")
def ingest_data(db: Session = Depends(get_db)):
    try:
        records = fetch_and_ingest(db)
        return {"status": "success", "records_processed": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    try:
        offset = (page - 1) * limit
        customers = db.query(Customer).offset(offset).limit(limit).all()
        total = db.query(Customer).count()
        return {
            "data": customers,
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception:
        # Gracefully return empty if dlt hasn't created the table yet
        return {"data": [], "total": 0, "page": page, "limit": limit}

@app.get("/api/customers/{id}")
def get_customer(id: str, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.customer_id == id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except Exception:
        raise HTTPException(status_code=404, detail="Customer not found")