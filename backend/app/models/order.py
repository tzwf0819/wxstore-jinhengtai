from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import NVARCHAR

from .base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_sn = Column(NVARCHAR(64), unique=True, index=True, nullable=False)
    user_id = Column(Integer)  # Assuming you have a User model and will add a ForeignKey
    total_amount = Column(Float, nullable=False)
    status = Column(NVARCHAR(50), default='PENDING')
    shipping_address = Column(NVARCHAR(255), nullable=False)
    shipping_contact = Column(NVARCHAR(255))
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
