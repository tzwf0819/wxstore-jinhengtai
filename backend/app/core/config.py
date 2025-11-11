from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQL_SERVER_HOST: str
    SQL_SERVER_PORT: int
    SQL_SERVER_USER: str
    SQL_SERVER_PASSWORD: str
    SQL_SERVER_DATABASE: str
    SQL_SERVER_DRIVER: str = "ODBC Driver 18 for SQL Server"

    class Config:
        env_file = ".env"

settings = Settings()
