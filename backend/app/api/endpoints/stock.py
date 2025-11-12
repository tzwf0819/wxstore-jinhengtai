
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ... import models
from ...api import deps
from ...schemas.stock import StockMovementRead, StockMovementCreate

router = APIRouter()

@router.get("/", response_model=List[StockMovementRead])
def list_stock_movements(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    movements = db.query(models.StockMovement).order_by(models.StockMovement.created_at.desc()).offset(skip).limit(limit).all()
    return movements

@router.post("/in", response_model=StockMovementRead)
def stock_in(movement: StockMovementCreate, db: Session = Depends(deps.get_db)):
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


@router.post("/void/{movement_id}", response_model=StockMovementRead)
def void_stock_movement(movement_id: int, db: Session = Depends(deps.get_db)):
    # 1. Find the original movement
    original_movement = db.get(models.StockMovement, movement_id)
    if not original_movement:
        raise HTTPException(status_code=404, detail="Stock movement not found")

    # 2. Check if it's already voided
    if original_movement.movement_type == StockMovementType.VOID.value or \
       (original_movement.reference_id and original_movement.reference_id.startswith("voided_by_")):
        raise HTTPException(status_code=400, detail="This movement has already been voided")

    # 3. Find the associated product
    product = db.get(models.Product, original_movement.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Associated product not found")

    # 4. Create a new, opposing movement to void the original one
    voiding_quantity = -original_movement.quantity
    void_movement = models.StockMovement(
        product_id=original_movement.product_id,
        quantity=voiding_quantity,
        movement_type=StockMovementType.VOID.value,
        reference_id=f"voids_{movement_id}"
    )
    db.add(void_movement)

    # 5. Update the product's stock quantity
    product.stock_quantity += voiding_quantity
    db.add(product)

    # Commit to get the ID for void_movement
    db.commit()
    db.refresh(void_movement)

    # 6. Mark the original movement as voided by updating its reference
    original_movement.reference_id = f"voided_by_{void_movement.id}"
    db.add(original_movement)
    db.commit()

    return void_movement

@router.post("/out-return", response_model=StockMovementRead)
def stock_out_return(movement: StockMovementCreate, db: Session = Depends(deps.get_db)):
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


@router.post("/void/{movement_id}", response_model=StockMovementRead)
def void_stock_movement(movement_id: int, db: Session = Depends(deps.get_db)):
    # 1. Find the original movement
    original_movement = db.get(models.StockMovement, movement_id)
    if not original_movement:
        raise HTTPException(status_code=404, detail="Stock movement not found")

    # 2. Check if it's already voided
    if original_movement.movement_type == StockMovementType.VOID.value or \
       (original_movement.reference_id and original_movement.reference_id.startswith("voided_by_")):
        raise HTTPException(status_code=400, detail="This movement has already been voided")

    # 3. Find the associated product
    product = db.get(models.Product, original_movement.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Associated product not found")

    # 4. Create a new, opposing movement to void the original one
    voiding_quantity = -original_movement.quantity
    void_movement = models.StockMovement(
        product_id=original_movement.product_id,
        quantity=voiding_quantity,
        movement_type=StockMovementType.VOID.value,
        reference_id=f"voids_{movement_id}"
    )
    db.add(void_movement)

    # 5. Update the product's stock quantity
    product.stock_quantity += voiding_quantity
    db.add(product)

    # Commit to get the ID for void_movement
    db.commit()
    db.refresh(void_movement)

    # 6. Mark the original movement as voided by updating its reference
    original_movement.reference_id = f"voided_by_{void_movement.id}"
    db.add(original_movement)
    db.commit()

    return void_movement
