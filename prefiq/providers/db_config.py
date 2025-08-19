# prefiq/providers/db_config.py

from typing import Literal, Optional, Union
from pydantic import BaseModel, Field, conint

class MariaDBSettings(BaseModel):
    DB_ENGINE: Literal["mariadb"] = "mariadb"
    DB_MODE: Literal["sync", "async"] = "sync"

    DB_HOST: str = "127.0.0.1"
    DB_PORT: conint(ge=1, le=65535) = 3306  # type: ignore[call-arg]
    DB_USER: str = "root"
    DB_PASS: str = ""
    DB_NAME: str

    # used by your async pool warmup; harmless if you’re in sync mode
    DB_POOL_WARMUP: int = Field(1, ge=0)

class SQLiteSettings(BaseModel):
    DB_ENGINE: Literal["sqlite"]
    # Built-in driver is sync-only in your stack right now
    DB_MODE: Literal["sync"] = "sync"

    # File path or ':memory:'
    DB_NAME: str = "app.sqlite"

    # Allow these to exist in Settings without failing validation
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_USER: Optional[str] = None
    DB_PASS: Optional[str] = None

# Discriminated by DB_ENGINE
DatabaseSettings = Union[MariaDBSettings, SQLiteSettings]
