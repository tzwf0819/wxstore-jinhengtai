from sqlalchemy import Column, Integer, String

from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    openid = Column(String(255), unique=True, index=True, nullable=False)
    nickname = Column(String(255), nullable=True)
    avatar_url = Column(String(255), nullable=True)
