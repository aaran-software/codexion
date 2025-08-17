# prefiq/settings/get_settings.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

class Settings(BaseSettings):
    TESTING: bool = False

    DB_ENGINE: str = "mariadb"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASS: str = "DbPass1@@"
    DB_NAME: str = "codexion_db"
    DB_MODE: str = "async"

    JWT_SECRET_KEY: str = "your-super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DB_POOL_WARMUP: int = Field(1, description="Number of connections to prewarm in async pool")

    LOG_LEVEL: str = "INFO"  # DEBUG | INFO | WARNING | ERROR
    LOG_FORMAT: str = "text"  # "json" or "text"
    LOG_NAMESPACE: str = "prefiq"  # base logger name
    LOG_COLOR: str = "auto"
    DB_CLOSE_ATEXIT: bool = True

    model_config = SettingsConfigDict(
        env_file=env_path,
        extra="allow"
    )

    @property
    def project_root(self) -> str:
        return os.path.dirname(env_path)

    # @property
    # def database_url(self) -> str:
    #     from cortex.core.dataserve import get_database_url
    #     return get_database_url()


@lru_cache()
def _get_cached_settings() -> Settings:
    return Settings()

def get_settings() -> Settings:
    if os.getenv("TESTING", "0").lower() in ("1", "true"):
        return Settings()
    return _get_cached_settings()

def clear_settings_cache():
    _get_cached_settings.cache_clear()
