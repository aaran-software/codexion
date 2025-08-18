# prefiq/providers/db_config.py
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field, conint

class DatabaseSettings(BaseModel):
    DB_ENGINE: Literal["mariadb"] = "mariadb"
    DB_MODE: Literal["sync", "async"] = "sync"

    DB_HOST: str = "127.0.0.1"
    DB_PORT: conint(ge=1, le=65535) = 3306  # type: ignore[call-arg]
    DB_USER: str = "root"
    DB_PASS: str = ""
    DB_NAME: str

    DB_POOL_WARMUP: int = Field(1, ge=0)
