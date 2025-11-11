from collections.abc import Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ... import models, schemas
from ...core.db import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[schemas.ProductRead])
def list_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    sort_by: str = Query("created_at", description="Sort by field (e.g., 'sales', 'created_at')"),
) -> list[schemas.ProductRead]:
    # Calculate offset
    offset = (page - 1) * page_size

    # Base query
    query = select(models.Product)

    # Sorting
    if sort_by == "sales":
        query = query.order_by(models.Product.sales.desc())
    else:  # Default to sorting by creation date
        query = query.order_by(models.Product.created_at.desc())

    # Apply pagination
    query = query.offset(offset).limit(page_size)

    # Execute query
    products: Sequence[models.Product] = db.scalars(query).all()

    return [schemas.ProductRead.model_validate(p) for p in products]
