from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.dialects.mssql import NVARCHAR

from .base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR(100), nullable=False, unique=True)
    icon_url = Column(NVARCHAR(512))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

