from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import get_settings
from ..models.base import Base  # Import the single Base instance

settings = get_settings()

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
