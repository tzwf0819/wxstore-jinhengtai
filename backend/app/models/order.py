from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="PENDING")
    # Shipping info
    shipping_address = Column(String(255), nullable=False)
    shipping_contact = Column(String(255), nullable=False)

    items = relationship("OrderItem", back_populates="order")
    owner = relationship("User")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False) # Price at the time of purchase

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
