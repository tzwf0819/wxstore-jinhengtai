from pydantic import BaseModel
from typing import List

# --- Schemas for creating an order ---
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    shipping_address: str
    shipping_contact: str

# --- Schemas for reading an order ---
class OrderItemRead(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderRead(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    shipping_address: str
    shipping_contact: str
    items: List[OrderItemRead] = []

    class Config:
        from_attributes = True
