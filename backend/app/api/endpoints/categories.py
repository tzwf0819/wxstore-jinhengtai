from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...api import deps
from ...models import Category
from ...schemas.category import CategoryRead, CategoryUpdate

router = APIRouter()


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(deps.get_db)) -> list[CategoryRead]:
    """Lists all active categories."""
    categories: Sequence[Category] = db.scalars(
        select(Category).where(Category.is_active == True).order_by(Category.sort_order.asc())
    ).all()
    return [CategoryRead.model_validate(category) for category in categories]


@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(
    name: str = Form(...),
    db: Session = Depends(deps.get_db),
) -> Category:
    """Creates a new category from form data."""
    # Check if category name already exists
    existing_category = db.execute(select(Category).where(Category.name == name)).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    new_category = Category(name=name)
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
    name: str = Form(...),
    db: Session = Depends(deps.get_db),
) -> Category:
    """Updates a category's name from form data."""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if the new name is already taken by another category
    if name != category.name:
        existing_category = db.execute(select(Category).where(Category.name == name)).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    category.name = name
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
