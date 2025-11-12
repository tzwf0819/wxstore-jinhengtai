from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock_quantity: int
    image_url: str | None = None
    category: str | None = None
    sales: int | None = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock_quantity: int | None = None
    image_url: str | None = None
    category: str | None = None


class ProductRead(ProductBase):
    id: int
    current_stock: int = 0

    class Config:
        from_attributes = True


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
