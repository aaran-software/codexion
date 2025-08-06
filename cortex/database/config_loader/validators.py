# =============================================================
# Database Config Validators (validators.py)
# =============================================================

from typing import Any
from .drivers import mariadb, postgresql, sqlite, mongodb

# Optional: if using with Pydantic, import validator
# from pydantic import validator

DRIVER_CONFIG_MAP = {
    "mariadb": mariadb.get_config,
    "postgresql": postgresql.get_config,
    "sqlite": sqlite.get_config,
    "mongodb": mongodb.get_config,
}


class DatabaseValidators:
    """Centralized validation methods for DatabaseConfig"""

    @staticmethod
    def validate_driver(v: str) -> str:
        v = v.lower()
        if v not in DRIVER_CONFIG_MAP:
            raise ValueError(
                f"Unsupported driver '{v}'. Must be one of: {list(DRIVER_CONFIG_MAP.keys())}"
            )
        return v

    @staticmethod
    def validate_port(v: int) -> int:
        if not 1 <= v <= 65535:
            raise ValueError(f"Invalid port {v}. Must be between 1-65535")
        return v

    @staticmethod
    def validate_pool_size(v: int) -> int:
        if v < 1:
            raise ValueError(f"Pool size {v} must be at least 1")
        return v

    @staticmethod
    def validate_host(v: str) -> str:
        if not v.strip():
            raise ValueError("Host cannot be empty")
        return v.strip()

    @staticmethod
    def validate_user(v: str) -> str:
        if not v.strip():
            raise ValueError("User cannot be empty")
        return v.strip()

    @staticmethod
    def validate_password(v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Password must be a string")
        return v
