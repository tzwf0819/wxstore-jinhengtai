from sqlalchemy import Column, DateTime, Float, Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import NVARCHAR

from .base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR(255), index=True)
    description = Column(NVARCHAR)
    price = Column(Float)
    stock_quantity = Column(Integer, default=0, nullable=False)
    sales = Column(Integer, default=0, nullable=False)
    image_url = Column(NVARCHAR(255), nullable=True)
    category = Column(NVARCHAR(100), nullable=True) # Simple text field for category
    created_at = Column(DateTime, server_default=func.now())

    items = relationship("OrderItem", back_populates="product")
