from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models import Category
from ...schemas.category import CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)) -> list[CategoryRead]:
    categories: Sequence[Category] = db.scalars(
        select(Category).where(Category.is_active.is_(True)).order_by(Category.sort_order.asc())
    ).all()

    return [CategoryRead.model_validate(category) for category in categories]
