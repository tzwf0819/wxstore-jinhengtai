from fastapi import APIRouter

# Import all the endpoint modules
from .endpoints import banners, categories, orders, products, uploads, stock, admin # Add admin

api_router = APIRouter()

# Include all the routers from the endpoints
api_router.include_router(banners.router, prefix="/banners", tags=["Banners"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["Uploads"]) # Add uploads router
api_router.include_router(stock.router, prefix="/stock", tags=["Stock"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
