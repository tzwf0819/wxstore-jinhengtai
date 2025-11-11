from functools import lru_cache

from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    app_name: str = "Jinhengtai Mall Backend"
    debug: bool = False
    api_base_url: str = "https://api.jinhengtai.yidasoftware.xyz"
    sql_server_host: str = "152.136.13.33"
    sql_server_port: int = 1433
    sql_server_user: str = "sa"
    sql_server_password: str = "YourStrong@Passw0rd"
    sql_server_database: str = "mall_db"
    sql_server_driver: str = "ODBC Driver 18 for SQL Server"
    sql_server_encrypt: str = "yes"
    sql_server_trust_server_certificate: str = "no"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> URL:
        return URL.create(
            "mssql+pyodbc",
            username=self.sql_server_user,
            password=self.sql_server_password,
            host=self.sql_server_host,
            port=self.sql_server_port,
            database=self.sql_server_database,
            query={
                "driver": self.sql_server_driver,
                "Encrypt": self.sql_server_encrypt,
                "TrustServerCertificate": self.sql_server_trust_server_certificate,
            },
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
