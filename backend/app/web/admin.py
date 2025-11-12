import os
import shutil
import uuid
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import pathlib

from .. import models, schemas
from ..api import deps
from ..api.endpoints import products as api_products

router = APIRouter()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

UPLOADS_DIR = BASE_DIR / "static" / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/admin", response_class=HTMLResponse)
async def admin_home(request: Request):
    return RedirectResponse(url="/admin/products")

@router.get("/admin/products", response_class=HTMLResponse)
async def list_products_web(request: Request, db: Session = Depends(deps.get_db)):
    products_data = api_products.get_all_products(
        db=db, page=1, page_size=200, sort_by='created_at', sort_order='desc', category=None
    )
    return templates.TemplateResponse("product_list.html", {"request": request, "products": products_data})

@router.get("/admin/products/edit/{product_id}", response_class=HTMLResponse)
async def edit_product_form(request: Request, product_id: int, db: Session = Depends(deps.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    return templates.TemplateResponse(
        "product_form.html", 
        {"request": request, "product": product, "is_edit": True, "ROOT_PATH": os.getenv("ROOT_PATH", "")}
    )

@router.get("/admin/products/new", response_class=HTMLResponse)
async def new_product_form(request: Request):
    return templates.TemplateResponse("product_form.html", {"request": request, "product": None, "is_edit": False})

@router.post("/admin/products/new")
async def create_product_web(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    category: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(deps.get_db)
):
    image_url = None
    if image and image.filename:
        unique_filename = f"{uuid.uuid4()}_{image.filename}"
        file_path = UPLOADS_DIR / unique_filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/uploads/{unique_filename}"

    product_in = schemas.ProductCreate(
        name=name, description=description, price=price, category=category, 
        image_url=image_url, stock_quantity=0
    )
    api_products.create_product(product_in=product_in, db=db)
    return RedirectResponse(url="/admin/products", status_code=303)

@router.post("/admin/products/edit/{product_id}")
async def update_product_web(
    product_id: int,
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    category: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(deps.get_db)
):
    db_product = db.get(models.Product, product_id)
    if not db_product:
        return HTMLResponse(status_code=404, content="Product not found")

    image_url = db_product.image_url
    if image and image.filename:
        unique_filename = f"{uuid.uuid4()}_{image.filename}"
        file_path = UPLOADS_DIR / unique_filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/uploads/{unique_filename}"

    product_in = schemas.ProductUpdate(
        name=name, description=description, price=price, category=category, 
        image_url=image_url
    )
    api_products.update_product(product_id=product_id, product_in=product_in, db=db)
    return RedirectResponse(url="/admin/products", status_code=303)

# ... (The rest of the admin routes will be added in the next step)
