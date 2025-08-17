from __future__ import annotations
from pydantic import BaseModel, Field, field_validator

_ALLOWED_ENGINES = {"mariadb"}  # keep strict for now (expand when other engines ship)
_ALLOWED_MODES = {"async", "sync"}

class DatabaseSettings(BaseModel):
    DB_ENGINE: str = Field(..., description="Database engine", examples=["mariadb"])
    DB_MODE: str = Field(..., description="Engine mode", examples=["async", "sync"])
    DB_HOST: str = Field(..., min_length=1, description="Hostname or IP")
    DB_PORT: int = Field(..., ge=1, le=65535, description="TCP port")
    DB_USER: str = Field(..., min_length=1, description="Username")
    DB_PASS: str = Field(..., min_length=0, description="Password (can be empty)")
    DB_NAME: str = Field(..., min_length=1, description="Database name")

    @field_validator("DB_ENGINE")
    @classmethod
    def _engine_ok(cls, v: str) -> str:
        v = v.lower()
        if v not in _ALLOWED_ENGINES:
            raise ValueError(f"Unsupported DB_ENGINE '{v}'. Allowed: {sorted(_ALLOWED_ENGINES)}")
        return v

    @field_validator("DB_MODE")
    @classmethod
    def _mode_ok(cls, v: str) -> str:
        v = v.lower()
        if v not in _ALLOWED_MODES:
            raise ValueError(f"Unsupported DB_MODE '{v}'. Allowed: {sorted(_ALLOWED_MODES)}")
        return v
