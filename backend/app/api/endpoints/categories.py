from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...api import deps
from ...models import Category
from ...schemas.category import CategoryRead, CategoryCreate, CategoryUpdate

router = APIRouter()


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(deps.get_db)) -> list[CategoryRead]:
    """Lists all active categories."""
    categories: Sequence[Category] = db.scalars(
        select(Category).where(Category.is_active == True).order_by(Category.sort_order.asc())
    ).all()
    return [CategoryRead.model_validate(category) for category in categories]


@router.post("/", response_model=CategoryRead, status_code=200)
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(deps.get_db),
) -> Category:
    """Creates a new category from JSON data."""
    existing_category = db.execute(select(Category).where(Category.name == category_in.name)).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    new_category = Category(name=category_in.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(deps.get_db)) -> Category:
    """Gets a single category by its ID."""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: Session = Depends(deps.get_db),
) -> Category:
    """Updates a category's name from JSON data."""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category_in.name != category.name:
        existing_category = db.execute(select(Category).where(Category.name == category_in.name)).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    category.name = category_in.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(deps.get_db)) -> None:
    """Deletes a category."""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
