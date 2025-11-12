import os
import shutil
import uuid
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import pathlib

from .. import models
from ..schemas import banner as banner_schemas
from ..api import deps
from ..api.endpoints import products as api_products, banners as api_banners, categories as api_categories, orders as api_orders, stock as api_stock

router = APIRouter()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

UPLOADS_DIR = BASE_DIR / "static" / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/admin", response_class=HTMLResponse)
async def admin_home(request: Request):
    return RedirectResponse(url=request.url_for('list_products_web'))

@router.get("/admin/products", response_class=HTMLResponse)
async def list_products_web(request: Request, db: Session = Depends(deps.get_db)):
    products_data = api_products.get_all_products(
        db=db, page=1, page_size=200, sort_by='created_at', sort_order='desc', category=None
    )
    return templates.TemplateResponse("product_list.html", {"request": request, "products": products_data})

@router.get("/admin/products/edit/{product_id}", response_class=HTMLResponse)
async def edit_product_form(request: Request, product_id: int, db: Session = Depends(deps.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    return templates.TemplateResponse("product_form.html", {"request": request, "product": product, "is_edit": True})

@router.get("/admin/products/new", response_class=HTMLResponse)
async def new_product_form(request: Request):
    return templates.TemplateResponse("product_form.html", {"request": request, "product": None, "is_edit": False})

@router.post("/admin/products/new")
async def create_product_web(
    request: Request,
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
    return RedirectResponse(url=request.url_for('list_products_web'), status_code=303)

@router.post("/admin/products/edit/{product_id}")
async def update_product_web(
    request: Request,
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
    return RedirectResponse(url=request.url_for('list_products_web'), status_code=303)

# --- Banner Management Routes ---

@router.get("/admin/banners", response_class=HTMLResponse)
async def list_banners_web(request: Request, db: Session = Depends(deps.get_db)):
    banners_data = api_banners.read_banners(db=db)
    return templates.TemplateResponse("banner_list.html", {"request": request, "banners": banners_data})

@router.get("/admin/banners/new", response_class=HTMLResponse)
async def new_banner_form(request: Request):
    return templates.TemplateResponse("banner_form.html", {"request": request, "banner": None, "is_edit": False})

@router.post("/admin/banners/new")
async def create_banner_web(
    request: Request,
    link_url: str = Form(None),
    sort_order: int = Form(1),
    is_active: bool = Form(False),
    image: UploadFile = File(...),
    db: Session = Depends(deps.get_db)
):
    image_url = None
    if image and image.filename:
        unique_filename = f"{uuid.uuid4()}_{image.filename}"
        file_path = UPLOADS_DIR / unique_filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/uploads/{unique_filename}"

    banner_in = banner_schemas.BannerCreate(
        image_url=image_url,
        link_url=link_url,
        sort_order=sort_order,
        is_active=is_active,
    )
    api_banners.create_banner(db=db, banner_in=banner_in)
    return RedirectResponse(url=request.url_for('list_banners_web'), status_code=303)

@router.get("/admin/banners/edit/{banner_id}", response_class=HTMLResponse)
async def edit_banner_form(request: Request, banner_id: int, db: Session = Depends(deps.get_db)):
    banner = db.query(models.Banner).filter(models.Banner.id == banner_id).first()
    if not banner:
        return HTMLResponse(status_code=404, content="Banner not found")
    return templates.TemplateResponse("banner_form.html", {"request": request, "banner": banner, "is_edit": True})

@router.post("/admin/banners/edit/{banner_id}")
async def update_banner_web(
    request: Request,
    banner_id: int,
    link_url: str = Form(None),
    sort_order: int = Form(1),
    is_active: str = Form(None), # Receive as string to handle checkbox
    image: UploadFile = File(None),
    db: Session = Depends(deps.get_db)
):
    db_banner = db.get(models.Banner, banner_id)
    if not db_banner:
        return HTMLResponse(status_code=404, content="Banner not found")

    image_url = db_banner.image_url
    if image and image.filename:
        unique_filename = f"{uuid.uuid4()}_{image.filename}"
        file_path = UPLOADS_DIR / unique_filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/uploads/{unique_filename}"

    # Convert is_active from form value ('true' or None) to boolean
    is_active_bool = is_active == 'true'

    banner_in = banner_schemas.BannerUpdate(
        image_url=image_url,
        link_url=link_url,
        sort_order=sort_order,
        is_active=is_active_bool,
    )
    api_banners.update_banner(db=db, banner_id=banner_id, banner_in=banner_in)
    return RedirectResponse(url=request.url_for('list_banners_web'), status_code=303)


@router.post("/admin/banners/delete/{banner_id}")
async def delete_banner_web(request: Request, banner_id: int, db: Session = Depends(deps.get_db)):
    api_banners.delete_banner(db=db, banner_id=banner_id)
    return RedirectResponse(url=request.url_for('list_banners_web'), status_code=303)


# --- Category Management Routes ---

@router.get("/admin/categories", response_class=HTMLResponse)
async def list_categories_web(request: Request, db: Session = Depends(deps.get_db)):
    categories_data = api_categories.list_categories(db=db)
    return templates.TemplateResponse("category_list.html", {"request": request, "categories": categories_data})

@router.get("/admin/categories/new", response_class=HTMLResponse)
async def new_category_form(request: Request):
    return templates.TemplateResponse("category_form.html", {"request": request, "category": None, "is_edit": False})

@router.post("/admin/categories/new")
async def create_category_web(
    request: Request,
    name: str = Form(...),
    db: Session = Depends(deps.get_db)
):
    category_in = schemas.CategoryCreate(name=name)
    api_categories.create_category(db=db, category_in=category_in)
    return RedirectResponse(url=request.url_for('list_categories_web'), status_code=303)

@router.get("/admin/categories/edit/{category_id}", response_class=HTMLResponse)
async def edit_category_form(request: Request, category_id: int, db: Session = Depends(deps.get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        return HTMLResponse(status_code=404, content="Category not found")
    return templates.TemplateResponse("category_form.html", {"request": request, "category": category, "is_edit": True})

@router.post("/admin/categories/edit/{category_id}")
async def update_category_web(
    request: Request,
    category_id: int,
    name: str = Form(...),
    db: Session = Depends(deps.get_db)
):
    category_in = schemas.CategoryUpdate(name=name)
    updated_category = api_categories.update_category(db=db, category_id=category_id, category_in=category_in)
    if not updated_category:
        return HTMLResponse(status_code=404, content="Category not found")
    return RedirectResponse(url=request.url_for('list_categories_web'), status_code=303)

@router.post("/admin/categories/delete/{category_id}")
async def delete_category_web(request: Request, category_id: int, db: Session = Depends(deps.get_db)):
    api_categories.delete_category(db=db, category_id=category_id)
    return RedirectResponse(url=request.url_for('list_categories_web'), status_code=303)


# --- Order Management Routes (Read-Only) ---

@router.get("/admin/orders", response_class=HTMLResponse)
async def list_orders_web(request: Request, db: Session = Depends(deps.get_db)):
    orders_data = api_orders.read_orders(db=db, skip=0, limit=100) # Fetch latest 100 orders
    return templates.TemplateResponse("order_list.html", {"request": request, "orders": orders_data})

@router.get("/admin/orders/{order_id}", response_class=HTMLResponse)
async def view_order_web(request: Request, order_id: int, db: Session = Depends(deps.get_db)):
    order = api_orders.read_order(db=db, order_id=order_id)
    if not order:
        return HTMLResponse(status_code=404, content="Order not found")
    return templates.TemplateResponse("order_detail.html", {"request": request, "order": order})


# --- Stock Management Routes (Read-Only) ---

@router.get("/admin/stock", response_class=HTMLResponse)
async def list_stock_movements_web(request: Request, db: Session = Depends(deps.get_db)):
    stock_movements = api_stock.list_stock_movements(db=db, skip=0, limit=200) # Fetch latest 200 movements
    return templates.TemplateResponse("stock_list.html", {"request": request, "movements": stock_movements})
