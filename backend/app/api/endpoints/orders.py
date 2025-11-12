
import time
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from ... import models
from ...core.database import get_db
from ...schemas.order import OrderCreate, OrderRead
from ...schemas.stock import StockMovementCreate
from ...models.stock import StockMovementType

router = APIRouter()

@router.post("/", response_model=OrderRead)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
):
    total_amount = 0
    order_items_to_create = []

    # First, validate all products and calculate total amount
    for item_in in order_in.items:
        product = db.get(models.Product, item_in.product_id)
        if not product:
            raise HTTPException(
                status_code=404, 
                detail=f"Product with id {item_in.product_id} not found"
            )
        if product.stock_quantity < item_in.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough stock for product {product.name}. Available: {product.stock_quantity}, Requested: {item_in.quantity}"
            )
        total_amount += product.price * item_in.quantity

    order_sn = f"{int(time.time() * 1000)}{random.randint(100, 999)}"
    user_id = 1 # Replace with real user logic later

    db_order = models.Order(
        order_sn=order_sn,  
        user_id=user_id,      
        total_amount=total_amount,
        shipping_address=order_in.shipping_address,
        shipping_contact=order_in.shipping_contact,
        status="PENDING",
    )
    db.add(db_order)
    db.flush()

    for item_in in order_in.items:
        product = db.get(models.Product, item_in.product_id)
        product.stock_quantity -= item_in.quantity
        product.sales += item_in.quantity
        
        order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            quantity=item_in.quantity,
            price=product.price
        )
        order_items_to_create.append(order_item)

        sale_movement = models.StockMovement(
            product_id=product.id,
            quantity=-item_in.quantity, 
            movement_type=StockMovementType.SALE.value,
            reference_id=f"order_{db_order.id}"
        )
        db.add(sale_movement)
    
    db.add_all(order_items_to_create)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[OrderRead])
def read_orders(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    orders = (
        db.query(models.Order)
        .options(joinedload(models.Order.items).joinedload(models.OrderItem.product))
        .order_by(models.Order.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return orders

@router.get("/{order_id}", response_model=OrderRead)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = (
        db.query(models.Order)
        .options(joinedload(models.Order.items).joinedload(models.OrderItem.product))
        .filter(models.Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/{order_id}/delete", status_code=204)
def delete_order_via_post(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).options(joinedload(models.Order.items)).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for item in order.items:
        # Restore stock and decrease sales for the refunded product
        product = db.get(models.Product, item.product_id)
        if product:
            product.stock_quantity += item.quantity
            product.sales -= item.quantity
            db.add(product)

        # Create a stock movement record for the refund
        refund_movement = models.StockMovement(
            product_id=item.product_id,
            quantity=item.quantity,  # Positive quantity for refund
            movement_type=StockMovementType.REFUND.value,
            reference_id=f"order_{order.id}"
        )
        db.add(refund_movement)

    db.delete(order)
    db.commit()
    return
