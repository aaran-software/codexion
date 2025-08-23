# prefiq/settings/get_settings.py
from __future__ import annotations

import os
from functools import lru_cache
from typing import Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve the repo .env once; allow an override via ENV_FILE if you need a different path.
_DEFAULT_ENV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", ".env")
)
_ENV_FILE = os.getenv("ENV_FILE", _DEFAULT_ENV_PATH)


class Settings(BaseSettings):
    # --- meta/env ---
    ENV: Literal["development", "test", "production"] = "development"
    TESTING: bool = False  # tip: set TESTING=1 under pytest

    # --- database ---
    DB_ENGINE: Literal["mariadb", "mysql", "sqlite", "postgres"] = "mariadb"
    DB_MODE: Literal["sync", "async"] = "async"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASS: str = "DbPass1@@"
    DB_NAME: str = "codexion_db"

    # Async pool warmup (harmless/no-op for sync engines)
    DB_POOL_WARMUP: int = Field(
        1, ge=0, description="Number of connections to prewarm in async pool"
    )

    # --- jwt/auth (defaults OK for local dev only) ---
    JWT_SECRET_KEY: str = "your-super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- logging ---
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    LOG_FORMAT: Literal["json", "text"] = "text"
    LOG_NAMESPACE: str = "prefiq"
    LOG_COLOR: Literal["auto", "true", "false"] = "auto"

    # --- misc toggles ---
    DB_CLOSE_ATEXIT: bool = True

    # pydantic-settings v2 config
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,   # env var *names* are case-insensitive
        extra="allow",
    )

    # --- computed helpers ----------------------------------------------------

    @property
    def project_root(self) -> str:
        return os.path.dirname(_DEFAULT_ENV_PATH)

    @property
    def is_async(self) -> bool:
        return self.DB_MODE.lower() == "async"

    # Normalize a few fields (defensive; supports common env variants)

    @field_validator("DB_ENGINE", mode="before")
    @classmethod
    def _normalize_engine(cls, v: str) -> str:
        v = (v or "").lower()
        aliases = {"postgresql": "postgres", "sqlite3": "sqlite", "pg": "postgres"}
        return aliases.get(v, v)

    @field_validator("DB_MODE", mode="before")
    @classmethod
    def _normalize_mode(cls, v: str) -> str:
        return (v or "").lower()

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def _normalize_log_level(cls, v: str) -> str:
        # accept 'debug', 'warn', etc.
        s = (v or "").strip().lower()
        map_alias = {
            "debug": "DEBUG",
            "info": "INFO",
            "warning": "WARNING",
            "warn": "WARNING",
            "error": "ERROR",
            "err": "ERROR",
        }
        return map_alias.get(s, s.upper())

    @field_validator("LOG_FORMAT", mode="before")
    @classmethod
    def _normalize_log_format(cls, v: str) -> str:
        # accept 'JSON'/'Text'
        s = (v or "").strip().lower()
        if s in {"json", "text"}:
            return s
        return s or "text"

    @field_validator("LOG_COLOR", mode="before")
    @classmethod
    def _normalize_log_color(cls, v: str) -> str:
        # accept booleans/on/off/1/0 in addition to 'auto'
        s = (v or "").strip().lower()
        if s in {"auto", "true", "false"}:
            return s
        if s in {"1", "yes", "y", "on"}:
            return "true"
        if s in {"0", "no", "n", "off"}:
            return "false"
        return "auto" if not s else s

    # Example DSN helpers (optional; keep if useful elsewhere)
    def dsn(self) -> Optional[str]:
        if self.DB_ENGINE == "sqlite":
            # You use DB_NAME as file path or ':memory:' in your stack.
            return f"sqlite:///{self.DB_NAME}"
        if self.DB_ENGINE in {"mariadb", "mysql"}:
            return f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        if self.DB_ENGINE == "postgres":
            # libpq-style URL
            return (
                f"postgresql://{self.DB_USER}:{self.DB_PASS}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        return None


# --- cached loader API (stable import surface) -------------------------------

@lru_cache()
def _load_cached_settings() -> Settings:
    return Settings()


def load_settings(*, force_refresh: bool = False) -> Settings:
    """
    App-wide cached settings. For tests set TESTING=1 or pass force_refresh=True.
    """
    if force_refresh or os.getenv("TESTING", "0").lower() in ("1", "true", "yes"):
        # fresh object each time during tests when you ask for it
        return Settings()
    return _load_cached_settings()


def clear_settings_cache() -> None:
    _load_cached_settings.cache_clear()
