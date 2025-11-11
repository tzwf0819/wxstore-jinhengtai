from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ... import models, schemas
from ...api import deps

router = APIRouter()

@router.post("/in", response_model=schemas.StockMovementRead)
def stock_in(movement: schemas.StockMovementCreate, db: Session = Depends(deps.get_db)):
    product = db.get(models.Product, movement.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update product stock
    product.stock_quantity += movement.quantity

    # Create stock movement record
    db_movement = models.StockMovement(
        product_id=movement.product_id,
        quantity=movement.quantity,
        movement_type='stock_in',
        reference_id=movement.reference_id
    )
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

@router.post("/out-return", response_model=schemas.StockMovementRead)
def stock_out_return(movement: schemas.StockMovementCreate, db: Session = Depends(deps.get_db)):
    product = db.get(models.Product, movement.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock_quantity < movement.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock for return")

    # Update product stock
    product.stock_quantity -= movement.quantity

    # Create stock movement record
    db_movement = models.StockMovement(
        product_id=movement.product_id,
        quantity=movement.quantity,
        movement_type='stock_out_return',
        reference_id=movement.reference_id
    )
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement
