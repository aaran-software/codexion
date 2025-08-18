# prefiq/database/dialects/registry.py

from __future__ import annotations
from typing import Optional

from prefiq.database.connection_manager import get_engine
from prefiq.database.dialects.base import Dialect
from prefiq.database.dialects.sqlite import SQLiteDialect
from prefiq.database.dialects.mysql import MySQLDialect
from prefiq.database.dialects.mariadb import MariaDBDialect
# (Optional) add others if you have them:
# from prefiq.database.dialects.postgres import PostgresDialect
# from prefiq.database.dialects.mongodb import MongoDBDialect

# Optional override for tests / forcing a dialect
_FORCED: Optional[str] = None


def set_dialect_for_tests(name: Optional[str]) -> None:
    """Force a specific dialect by name for tests (e.g., 'sqlite', 'mysql', 'mariadb')."""
    global _FORCED
    _FORCED = name.lower() if name else None


def _from_engine_name(name: str) -> Dialect:
    """
    Map an engine/backend/url string to a specific Dialect.
    IMPORTANT: check 'mariadb' BEFORE 'mysql' so MariaDB isn't misclassified.
    """
    n = name.lower()

    # Exact family checks first
    if "mariadb" in n:
        return MariaDBDialect()
    if "mysql" in n:
        return MySQLDialect()

    # Optional extras (uncomment if you support them)
    # if "postgresql" in n or "postgres" in n or "psql" in n:
    #     return PostgresDialect()
    # if "mongodb" in n or "mongo" in n:
    #     return MongoDBDialect()

    # SQLite (also handle file/memory hints)
    if "sqlite" in n or n in ("file", "memory", ":memory:"):
        return SQLiteDialect()

    # Safe default
    return SQLiteDialect()


def get_dialect() -> Dialect:
    """
    Resolve the active dialect:

    1) If a test override is set, use that.
    2) Otherwise, inspect the engine object returned by get_engine().
       We try several common attributes (dialect_name, name, driver, backend, url/database_url/dsn).
    3) Fall back to SQLite if we can't tell.
    """
    # 1) explicit override for tests
    if _FORCED:
        return _from_engine_name(_FORCED)

    # 2) infer from engine object
    eng = get_engine()

    # First pass: explicit name-like attributes
    for attr in ("dialect_name", "name", "driver", "backend"):
        v = getattr(eng, attr, None)
        if isinstance(v, str) and v.strip():
            return _from_engine_name(v)

    # Second pass: URL/DSN-like attributes
    for attr in ("url", "database_url", "dsn"):
        v = getattr(eng, attr, None)
        if isinstance(v, str) and v.strip():
            return _from_engine_name(v)

    # 3) fallback
    return SQLiteDialect()
