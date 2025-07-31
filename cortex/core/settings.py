from pydantic_settings import BaseSettings
from functools import lru_cache
import os

# Path to .env file (2 levels up from this file)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


class Settings(BaseSettings):
    DB_ENGINE: str = "sqlite"
    DB_NAME: str = "codexion.db"
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    JWT_SECRET_KEY: str = "your-super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def project_root(self) -> str:
        return os.path.dirname(env_path)

    @property
    def database_url(self) -> str:
        from cortex.core.dataserve import get_database_url
        return get_database_url()

    class Config:
        env_file = env_path
        extra = "allow"


@lru_cache()
def get_settings():
    return Settings()
