from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from .. import models
from ..api import deps

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin", response_class=HTMLResponse)
async def admin_home(request: Request):
    return templates.TemplateResponse("admin_home.html", {"request": request})

from ..api.endpoints import products as api_products

@router.get("/admin/products", response_class=HTMLResponse)
async def list_products_web(request: Request, db: Session = Depends(deps.get_db)):
    products_data = api_products.list_products(
        db=db,
        page=1,          # Provide a default page number
        page_size=200,   # Provide a default page size
        sort_by='created_at',
        sort_order='desc'
    )
    return templates.TemplateResponse("product_list.html", {"request": request, "products": products_data})

@router.get("/admin/products/edit/{product_id}", response_class=HTMLResponse)
async def edit_product_form(request: Request, product_id: int, db: Session = Depends(deps.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    categories = db.query(models.Category).order_by(models.Category.name.asc()).all()
    return templates.TemplateResponse("product_form.html", {"request": request, "product": product, "categories": categories, "is_edit": True})

@router.get("/admin/products/new", response_class=HTMLResponse)
async def new_product_form(request: Request, db: Session = Depends(deps.get_db)):
    categories = db.query(models.Category).order_by(models.Category.name.asc()).all()
    return templates.TemplateResponse("product_form.html", {"request": request, "product": None, "categories": categories, "is_edit": False})

@router.get("/admin/banners", response_class=HTMLResponse)
async def list_banners_web(request: Request, db: Session = Depends(deps.get_db)):
    banners = db.query(models.Banner).order_by(models.Banner.sort_order.asc()).all()
    return templates.TemplateResponse("banner_list.html", {"request": request, "banners": banners})

@router.get("/admin/banners/new", response_class=HTMLResponse)
async def new_banner_form(request: Request):
    return templates.TemplateResponse("banner_form.html", {"request": request, "banner": None, "is_edit": False})

@router.get("/admin/banners/edit/{banner_id}", response_class=HTMLResponse)
async def edit_banner_form(request: Request, banner_id: int, db: Session = Depends(deps.get_db)):
    banner = db.query(models.Banner).filter(models.Banner.id == banner_id).first()
    return templates.TemplateResponse("banner_form.html", {"request": request, "banner": banner, "is_edit": True})

@router.get("/admin/stock", response_class=HTMLResponse)
async def list_stock_web(request: Request, db: Session = Depends(deps.get_db)):
    movements = db.query(models.StockMovement).options(joinedload(models.StockMovement.product)).order_by(models.StockMovement.created_at.desc()).all()
    return templates.TemplateResponse("stock_list.html", {"request": request, "movements": movements})

@router.get("/admin/stock/new", response_class=HTMLResponse)
async def new_stock_form(request: Request, db: Session = Depends(deps.get_db)):
    products = db.query(models.Product).order_by(models.Product.name.asc()).all()
    return templates.TemplateResponse("stock_form.html", {"request": request, "products": products})


@router.get("/admin/orders", response_class=HTMLResponse)
async def list_orders_web(request: Request, db: Session = Depends(deps.get_db)):
    orders = db.query(models.Order).options(
        joinedload(models.Order.items).joinedload(models.OrderItem.product)
    ).order_by(models.Order.id.desc()).all()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})


# --- Category Admin Routes ---

@router.get("/admin/categories", response_class=HTMLResponse)
async def list_categories_web(request: Request, db: Session = Depends(deps.get_db)):
    categories = db.query(models.Category).order_by(models.Category.name.asc()).all()
    return templates.TemplateResponse("category_list.html", {"request": request, "categories": categories})

@router.get("/admin/category/add", response_class=HTMLResponse)
async def new_category_form(request: Request):
    return templates.TemplateResponse("category_form.html", {"request": request, "category": None, "is_edit": False})

@router.get("/admin/category/edit/{category_id}", response_class=HTMLResponse)
async def edit_category_form(request: Request, category_id: int, db: Session = Depends(deps.get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    return templates.TemplateResponse("category_form.html", {"request": request, "category": category, "is_edit": True})


@router.post("/admin/category/add")
async def create_category_web(name: str = Form(...), db: Session = Depends(deps.get_db)):
    existing_category = db.execute(select(models.Category).where(models.Category.name == name)).first()
    if existing_category:
        # Here you might want to return an error to the user in the form
        # For now, we'll just redirect back with an error message (not implemented)
        return HTMLResponse(content=f"Category with name '{name}' already exists.", status_code=400)

    new_category = models.Category(name=name)
    db.add(new_category)
    db.commit()
    return RedirectResponse(url="/admin/categories", status_code=303)


@router.post("/admin/category/edit/{category_id}")
async def update_category_web(category_id: int, name: str = Form(...), db: Session = Depends(deps.get_db)):
    category = db.get(models.Category, category_id)
    if not category:
        return HTMLResponse(content="Category not found", status_code=404)

    if name != category.name:
        existing_category = db.execute(select(models.Category).where(models.Category.name == name)).first()
        if existing_category:
            return HTMLResponse(content=f"Category with name '{name}' already exists.", status_code=400)
    
    category.name = name
    db.commit()
    return RedirectResponse(url="/admin/categories", status_code=303)


@router.post("/admin/category/delete/{category_id}")
async def delete_category_web(category_id: int, db: Session = Depends(deps.get_db)):
    category = db.get(models.Category, category_id)
    if category:
        db.delete(category)
        db.commit()
    return RedirectResponse(url="/admin/categories", status_code=303)
