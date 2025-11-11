from pydantic import computed_field
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    SQL_SERVER_HOST: str
    SQL_SERVER_PORT: int = 1433
    SQL_SERVER_USER: str
    SQL_SERVER_PASSWORD: str
    SQL_SERVER_DATABASE: str
    SQL_SERVER_DRIVER: str = "ODBC Driver 18 for SQL Server"
    SQL_SERVER_ENCRYPT: str = "no"
    SQL_SERVER_TRUST_SERVER_CERTIFICATE: str = "yes"

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"mssql+pyodbc://{self.SQL_SERVER_USER}:{self.SQL_SERVER_PASSWORD}@"
            f"{self.SQL_SERVER_HOST}:{self.SQL_SERVER_PORT}/{self.SQL_SERVER_DATABASE}?"
            f"driver={self.SQL_SERVER_DRIVER.replace(' ', '+')}&"
            f"Encrypt={self.SQL_SERVER_ENCRYPT}&"
            f"TrustServerCertificate={self.SQL_SERVER_TRUST_SERVER_CERTIFICATE}"
        )

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
