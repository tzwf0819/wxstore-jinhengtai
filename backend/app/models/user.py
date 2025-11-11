from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mssql import NVARCHAR

from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    openid = Column(NVARCHAR(255), unique=True, index=True, nullable=False)
    nickname = Column(NVARCHAR(255), nullable=True)
    avatar_url = Column(NVARCHAR(255), nullable=True)
