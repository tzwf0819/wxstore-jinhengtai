from pydantic import BaseModel, Field
from typing import List, Optional

# --- Schemas for Products in Order ---
class ProductInfo(BaseModel):
    id: int
    name: str
    price: float
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

# --- Schemas for creating an order ---
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0) # Ensure quantity is positive

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    shipping_address: str
    shipping_contact: str

# --- Schemas for reading an order ---
class OrderItemRead(BaseModel):
    id: int
    quantity: int
    product: ProductInfo

    class Config:
        from_attributes = True

class OrderRead(BaseModel):
    id: int
    user_id: Optional[int] = None # User ID can be optional for now
    total_amount: float
    status: str
    shipping_address: str
    shipping_contact: str
    items: List[OrderItemRead] = []

    class Config:
        from_attributes = True
