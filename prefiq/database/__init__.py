# prefiq/database/__init__.py
"""
Database public API (back-compat shim + multi-engine helpers).

This module re-exports the commonly-used functions/classes so code that does:
    from prefiq.database import get_engine
continues to work even though the implementation lives in
prefiq.database.connection / connection_manager.
"""

from .connection import (
    get_engine,
    reset_engine,
    reload_engine_from_env,
    swap_engine,
    # named-engine helpers
    get_engine_named,
    reset_engine_named,
    swap_engine_named,
    engine_env,
)

from .connection_manager import (
    ConnectionManager,
    connection_manager,
    dev_connection_manager,
    analytics_connection_manager,
)

__all__ = [
    # core engine
    "get_engine", "reset_engine", "reload_engine_from_env", "swap_engine",
    # named engines
    "get_engine_named", "reset_engine_named", "swap_engine_named", "engine_env",
    # connection manager
    "ConnectionManager", "connection_manager",
    "dev_connection_manager", "analytics_connection_manager",
]
