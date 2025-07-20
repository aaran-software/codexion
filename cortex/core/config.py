from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DB_ENGINE: str = "sqlite"
    DB_NAME: str = "codexion.db"
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306

    @property
    def DATABASE_URL(self) -> str:
        from cortex.core.dataserve import get_database_url
        return get_database_url()

    class Config:
        env_file = "../.env"
        extra = "allow"

@lru_cache()
def get_settings():
    return Settings()
