# Import all schemas to make them accessible via app.schemas
from .banner import BannerRead, BannerCreate
from .category import CategoryRead
from .order import OrderRead, OrderCreate, OrderItemRead, OrderItemCreate
from .product import ProductRead, ProductCreate, ProductUpdate
from .stock import StockMovementCreate, StockMovementRead

__all__ = [
    "BannerRead",
    "BannerCreate",
    "CategoryRead",
    "OrderRead",
    "OrderCreate",
    "OrderItemRead",
    "OrderItemCreate",
    "ProductRead",
    "ProductCreate",
    "ProductUpdate",
    "StockMovementCreate",
    "StockMovementRead",
]
