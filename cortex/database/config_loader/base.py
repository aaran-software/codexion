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

from .drivers import mariadb, postgresql, sqlite, mongodb
from cortex.core.settings import get_settings

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

class DatabaseConfig:
    """
    Base configuration loader class for multiple database drivers.
    Supports defaults from global settings with the ability to override.
    """
    def __init__(
        self,
        driver: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        pool_size: Optional[int] = None,
        autocommit: Optional[bool] = True,
        uri: Optional[str] = None
    ):
        settings = get_settings()
        self._driver = (driver or settings.DB_ENGINE).lower()
        self._user = user or settings.DB_USER
        self._password = password or settings.DB_PASS
        self._host = host or settings.DB_HOST
        self._port = port or settings.DB_PORT
        self._database = database or settings.DB_NAME
        self._pool_size = pool_size or 5
        self._autocommit = autocommit
        self._uri = uri

    def get_config_dict(self) -> dict:
        """Returns the configuration dictionary for the selected driver."""
        if self._driver not in DRIVER_CONFIG_MAP:
            raise ValueError(f"Unsupported driver: {self._driver}")
        return DRIVER_CONFIG_MAP[self._driver](self)

    # Properties for attribute access
    @property
    def driver(self) -> str:
        return self._driver

    @driver.setter
    def driver(self, value: str):
        self._driver = value.lower()

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, value: str):
        self._user = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int):
        self._port = value

    @property
    def database(self) -> str:
        return self._database

    @database.setter
    def database(self, value: str):
        self._database = value

    @property
    def pool_size(self) -> int:
        return self._pool_size

    @pool_size.setter
    def pool_size(self, value: int):
        self._pool_size = value

    @property
    def autocommit(self) -> bool:
        return self._autocommit

    @autocommit.setter
    def autocommit(self, value: bool):
        self._autocommit = value

    @property
    def uri(self) -> Optional[str]:
        return self._uri

    @uri.setter
    def uri(self, value: str):
        self._uri = value

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
    override = deepcopy(current)
    for key, value in overrides.items():
        setattr(override, key, value)

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
    override = deepcopy(current)
    for key, value in overrides.items():
        setattr(override, key, value)

    push_async_config(override)
    try:
        yield override
    finally:
        pop_async_config()
