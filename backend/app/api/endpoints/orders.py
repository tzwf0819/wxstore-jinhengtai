from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.core.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # 此处应有更复杂的逻辑，例如库存检查、事务处理等
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
