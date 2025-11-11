from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.OrderRead)
def create_order(
    order_in: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    total_amount = 0
    order_items_to_create = []

    # Use a transaction to ensure all or nothing
    with db.begin_nested():
        for item_in in order_in.items:
            product = db.get(models.Product, item_in.product_id)
            if not product or not product.is_active:
                raise HTTPException(status_code=404, detail=f"Product with id {item_in.product_id} not found")
            
            # For simplicity, we are not handling stock here, but you would in a real app
            # if product.stock < item_in.quantity:
            #     raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")

            item_price = product.price
            total_amount += item_price * item_in.quantity

            order_item = models.OrderItem(
                product_id=product.id,
                quantity=item_in.quantity,
                price=item_price
            )
            order_items_to_create.append(order_item)

        # Create the main order
        db_order = models.Order(
            user_id=current_user.id,
            total_amount=total_amount,
            shipping_address=order_in.shipping_address,
            shipping_contact=order_in.shipping_contact,
            items=order_items_to_create
        )
        db.add(db_order)
    
    # The transaction is committed here upon exiting the `with` block successfully
    db.commit()
    db.refresh(db_order)
    return db_order
