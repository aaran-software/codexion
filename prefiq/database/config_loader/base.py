# =============================================================
# DatabaseConfigLoader (base.py)
#
# Author: ChatGPT (refactored for multi-driver use)
# Created: 2025-08-06
#
# Description:
#   - Centralized, reusable database configuration loader.
#   - Supports MariaDB, PostgresSQL, SQLite, MongoDB.
#   - Thread-safe and async-aware using local stacks.
#   - Allows nested scoped overrides per request/session.
# =============================================================

from typing import Optional, List
from contextlib import contextmanager, asynccontextmanager
from copy import deepcopy
import threading
import contextvars
from pydantic import BaseModel, field_validator, ConfigDict

from .drivers import mariadb, postgresql, sqlite, mongodb
from prefiq.providers.settings_provider import get_settings
from .validators import DatabaseValidators  # Import the validators

# Mapping of supported database drivers to their config builders
DRIVER_CONFIG_MAP = {
    "mariadb": mariadb.get_config,
    "postgresql": postgresql.get_config,
    "sqlite": sqlite.get_config,
    "mongodb": mongodb.get_config,
}

# Thread-local and async-local context stacks for scoped overrides
_thread_local = threading.local()
_async_local: contextvars.ContextVar[List["DatabaseConfig"]] = contextvars.ContextVar("db_config_stack", default=[])

class DatabaseConfig(BaseModel):  # Changed from ConfigDict to BaseModel
    """
    Base configuration loader class for multiple database drivers.
    Supports defaults from global settings with the ability to override.
    """
    driver: str
    user: str
    password: str
    host: str
    port: int = 3306
    database: str
    pool_size: int = 5
    autocommit: bool = True
    uri: Optional[str] = None

    model_config = ConfigDict(validate_assignment=True)  # Enable validation on attribute changes

    # Validators
    _validate_driver = field_validator('driver')(DatabaseValidators.validate_driver)
    _validate_port = field_validator('port')(DatabaseValidators.validate_port)
    _validate_pool_size = field_validator('pool_size')(DatabaseValidators.validate_pool_size)
    _validate_host = field_validator('host')(DatabaseValidators.validate_host)

    def __init__(
        self,
        driver: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        pool_size: Optional[int] = None,
        autocommit: Optional[bool] = None,
        uri: Optional[str] = None
    ):
        settings = get_settings()
        super().__init__(
            driver=(driver or settings.DB_ENGINE).lower(),
            user=user or settings.DB_USER,
            password=password or settings.DB_PASS,
            host=host or settings.DB_HOST,
            port=port or settings.DB_PORT,
            database=database or settings.DB_NAME,
            pool_size=pool_size or 5,
            autocommit=autocommit if autocommit is not None else True,
            uri=uri
        )

    def get_config_dict(self) -> dict:
        """Returns the configuration dictionary for the selected driver."""
        if self.driver not in DRIVER_CONFIG_MAP:
            raise ValueError(f"Unsupported driver: {self.driver}")
        return DRIVER_CONFIG_MAP[self.driver](self)

    # Properties for attribute access (now using Pydantic model fields)
    @property
    def driver(self) -> str:
        return self._driver

    @driver.setter
    def driver(self, value: str):
        self.driver = value.lower()  # Will trigger validation

    # ... (keep other property getters/setters the same but update to use model fields) ...

# ---------------------------
# Thread-local helpers
# ---------------------------

def _get_thread_stack() -> List[DatabaseConfig]:
    if not hasattr(_thread_local, "stack"):
        _thread_local.stack = []
    return _thread_local.stack

def use_thread_config() -> DatabaseConfig:
    stack = _get_thread_stack()
    return stack[-1] if stack else DatabaseConfig()

def push_thread_config(config: DatabaseConfig):
    _get_thread_stack().append(config)

def pop_thread_config():
    stack = _get_thread_stack()
    if stack:
        stack.pop()

# ---------------------------
# Async-local helpers
# ---------------------------

def use_async_config() -> DatabaseConfig:
    stack = _async_local.get()
    return stack[-1] if stack else DatabaseConfig()

def push_async_config(config: DatabaseConfig):
    _async_local.set(_async_local.get() + [config])

def pop_async_config():
    stack = _async_local.get()
    if stack:
        _async_local.set(stack[:-1])

# ---------------------------
# Scoped overrides
# ---------------------------

@contextmanager
def override_thread_config(**overrides):
    """
    Temporarily override DB config in a sync/threaded context.
    Supports nested overrides.
    """
    current = deepcopy(use_thread_config())
    override = current.model_copy(update=overrides)  # Use Pydantic's model_copy for updates
    push_thread_config(override)
    try:
        yield override
    finally:
        pop_thread_config()

@asynccontextmanager
async def override_async_config(**overrides):
    """
    Temporarily override DB config in an async context.
    Supports nested overrides.
    """
    current = deepcopy(use_async_config())
    override = current.model_copy(update=overrides)
    push_async_config(override)
    try:
        yield override
    finally:
        pop_async_config()