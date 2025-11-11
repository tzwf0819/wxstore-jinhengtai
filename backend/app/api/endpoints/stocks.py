from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.core.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{product_id}", response_model=schemas.Stock)
def read_stock(product_id: int, db: Session = Depends(get_db)):
    stock = db.query(models.Stock).filter(models.Stock.product_id == product_id).first()
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock
