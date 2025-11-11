from decimal import Decimal

from pydantic import BaseModel


from .category import CategoryRead


class ProductRead(BaseModel):
    id: int
    name: str
    code: str
    description: str | None
    price: Decimal
    cover_url: str | None
    stock: int
    sales: int
    is_active: bool
    categories: list[CategoryRead]

    class Config:
        from_attributes = True
