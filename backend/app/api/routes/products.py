from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models import Category, Product
from ...schemas.product import ProductRead

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductRead], summary="List products with filters")
def list_products(
    db: Session = Depends(get_db),
    *,
    category_code: str | None = Query(None, description="Filter by category code"),
    keyword: str | None = Query(None, description="Search by product name or description"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_by: str = Query("sales", pattern="^(sales|price|created_at)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
) -> list[ProductRead]:
    statement: Select[tuple[Product]] = select(Product).where(Product.is_active.is_(True))

    if category_code:
        statement = statement.join(Product.categories).where(Category.code == category_code)

    if keyword:
        pattern = f"%{keyword}%"
        statement = statement.where(
            or_(Product.name.ilike(pattern), Product.description.ilike(pattern))
        )

    sort_column = getattr(Product, sort_by)
    if sort_order == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    statement = (
        statement.order_by(sort_column)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .execution_options(populate_existing=True)
    )

    products: Sequence[Product] = db.scalars(statement).all()

    return [ProductRead.model_validate(product) for product in products]
