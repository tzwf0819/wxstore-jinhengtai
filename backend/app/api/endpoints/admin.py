from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from app import models
from app.core.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/orders")
def admin_orders(request: Request, db: Session = Depends(get_db)):
    orders = (
        db.query(models.Order)
        .options(joinedload(models.Order.items).joinedload(models.OrderItem.product))
        .order_by(models.Order.id.desc())
        .all()
    )
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})
