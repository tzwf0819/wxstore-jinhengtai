from collections.abc import Sequence
from datetime import datetime

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ... import models, schemas
from ...api import deps
from ...models.stock import StockMovement, StockMovementType

router = APIRouter()


@router.post("/", response_model=schemas.ProductRead)
def create_product(
    product_in: schemas.ProductCreate,
    db: Session = Depends(deps.get_db),
):
    # Create the product instance using stock_quantity
    db_product = models.Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        stock_quantity=product_in.stock_quantity, # Corrected field
        category=product_in.category,
        created_at=datetime.utcnow()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Create the initial stock movement record
    initial_movement = StockMovement(
        product_id=db_product.id,
        quantity=db_product.stock_quantity,
        movement_type=StockMovementType.INITIAL.value,
        reference_id="initial_setup"
    )
    db.add(initial_movement)
    db.commit()

    return schemas.ProductRead.model_validate(db_product)


@router.get("/{product_id}", response_model=schemas.ProductRead)
def read_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.ProductRead.model_validate(product)


@router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(
    product_id: int,
    product_in: schemas.ProductCreate, # Using Create schema is fine here
    db: Session = Depends(deps.get_db),
):
    db_product = db.get(models.Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_in.model_dump(exclude_unset=True)
    
    # Stock should be managed via dedicated stock endpoints.
    if 'stock_quantity' in update_data:
        del update_data['stock_quantity']

    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return schemas.ProductRead.model_validate(db_product)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
):
    # First, delete related stock movements to avoid integrity errors
    db.query(models.StockMovement).filter(models.StockMovement.product_id == product_id).delete(synchronize_session=False)

    db_product = db.get(models.Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return


@router.get("/", response_model=list[schemas.ProductRead])
def list_products(
    db: Session = Depends(deps.get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(200, ge=1, le=200, description="Page size"),
    sort_by: str = Query("created_at", description="Sort by field"),
    sort_order: str = Query("desc", description="Sort order (asc/desc)"),
) -> list[schemas.ProductRead]:
    offset = (page - 1) * page_size
    
    query = select(models.Product)

    sort_field = getattr(models.Product, sort_by, models.Product.created_at)
    if sort_order.lower() == "desc":
        query = query.order_by(sort_field.desc())
    else:
        query = query.order_by(sort_field.asc())

    query = query.offset(offset).limit(page_size)
    products: Sequence[models.Product] = db.scalars(query).all()

    product_reads = []
    for p in products:
        current_stock = db.query(func.sum(models.StockMovement.quantity)).filter(
            models.StockMovement.product_id == p.id
        ).scalar() or 0
        
        product_read = schemas.ProductRead.model_validate(p)
        product_read.current_stock = int(current_stock)
        product_reads.append(product_read)

    return product_reads
