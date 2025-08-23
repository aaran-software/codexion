# prefiq/database/dialects/registry.py
from __future__ import annotations
from typing import Optional

from prefiq.settings.get_settings import load_settings
from prefiq.database.connection_manager import get_engine

from prefiq.database.dialects.base import Dialect
from prefiq.database.dialects.sqlite import SQLiteDialect
from prefiq.database.dialects.mysql import MySQLDialect
from prefiq.database.dialects.mariadb import MariaDBDialect
from prefiq.database.dialects.postgres import PostgresDialect
# from prefiq.database.dialects.mongodb import MongoDBDialect  # not wired into SQL migrations

_FORCED: Optional[str] = None  # test override, e.g. set_dialect_for_tests("sqlite")


def set_dialect_for_tests(name: Optional[str]) -> None:
    global _FORCED
    _FORCED = name.lower() if name else None


def _from_name_fragment(name: str) -> Dialect:
    """Map a string (engine name/url/class) to a concrete Dialect.
       ORDER MATTERS: check 'mariadb' BEFORE 'mysql'."""
    n = (name or "").lower()

    # Distinguish MariaDB vs MySQL explicitly
    if "mariadb" in n:
        return MariaDBDialect()
    if "mysql" in n:
        return MySQLDialect()

    # Postgres
    if "postgresql" in n or "postgres" in n or "psql" in n:
        return PostgresDialect()

    # SQLite (file/memory hints too)
    if "sqlite" in n or n in ("file", "memory", ":memory:"):
        return SQLiteDialect()

    # Safe default for local/dev
    return SQLiteDialect()


def get_dialect() -> Dialect:
    # 0) explicit test override
    if _FORCED:
        return _from_name_fragment(_FORCED)

    # 1) honor explicit setting if provided
    s = load_settings()
    eng_setting = (getattr(s, "DB_ENGINE", "") or "").lower()
    if eng_setting:
        return _from_name_fragment(eng_setting)

    # 2) infer from engine object
    eng = get_engine()

    # first: attributes that often carry the backend name
    for attr in ("dialect_name", "name", "driver", "backend"):
        v = getattr(eng, attr, None)
        if isinstance(v, str) and v.strip():
            return _from_name_fragment(v)

    # second: URL/DSN-like attributes
    for attr in ("url", "database_url", "dsn"):
        v = getattr(eng, attr, None)
        if isinstance(v, str) and v.strip():
            return _from_name_fragment(v)

    # third: fall back to the class name / module (this fixes SyncMariaDBEngine cases)
    cls = type(eng)
    guess = f"{cls.__module__}.{cls.__name__}"
    return _from_name_fragment(guess)
