from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

DATABASE_URL = f"mssql+pyodbc://{settings.SQL_SERVER_USER}:{settings.SQL_SERVER_PASSWORD}@{settings.SQL_SERVER_HOST}:{settings.SQL_SERVER_PORT}/{settings.SQL_SERVER_DATABASE}?driver={settings.SQL_SERVER_DRIVER}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
