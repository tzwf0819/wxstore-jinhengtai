from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Jinhengtai Mall Backend"
    debug: bool = False
    sql_server_host: str = "152.136.13.33"
    sql_server_port: int = 1433
    sql_server_user: str = "sa"
    sql_server_password: str = "YourStrong@Passw0rd"
    sql_server_database: str = "mall_db"
    sql_server_driver: str = "ODBC Driver 17 for SQL Server"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        return (
            "mssql+pyodbc://"
            f"{self.sql_server_user}:{self.sql_server_password}@"
            f"{self.sql_server_host}:{self.sql_server_port}/"
            f"{self.sql_server_database}?driver={self.sql_server_driver.replace(' ', '+')}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
