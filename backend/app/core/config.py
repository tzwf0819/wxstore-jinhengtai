from pydantic import computed_field
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

def find_dotenv() -> str | None:
    """Find the .env file by searching upward from the current file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir != os.path.dirname(current_dir): # Stop at the root directory
        env_path = os.path.join(current_dir, ".env")
        if os.path.exists(env_path):
            return env_path
        current_dir = os.path.dirname(current_dir)
    return None

# Load .env file
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path=dotenv_path)
else:
    print("Warning: .env file not found. Using environment variables only.")


class Settings(BaseSettings):
    sql_server_host: str
    sql_server_port: int = 1433
    sql_server_user: str
    sql_server_password: str
    sql_server_database: str

    @computed_field
    @property
    def database_url(self) -> str:
        # 对密码进行URL编码，以处理特殊字符（如'@'）
        encoded_password = quote_plus(self.sql_server_password)
        driver = "ODBC Driver 18 for SQL Server".replace(' ', '+')

        return (
            f"mssql+pyodbc://{self.sql_server_user}:{encoded_password}@"
            f"{self.sql_server_host}:{self.sql_server_port}/{self.sql_server_database}?"
            f"driver={driver}&TrustServerCertificate=yes"
        )

@lru_cache
def get_settings():
    return Settings()
