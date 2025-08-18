# prefiq/database/dialects/registry.py
from __future__ import annotations
from typing import Optional
from prefiq.database.connection_manager import get_engine
from prefiq.database.dialects.sqlite import SQLiteDialect
from prefiq.database.dialects.mysql import MySQLDialect
from  prefiq.database.dialects.base import Dialect

# Optional override for tests / forcing a dialect
_FORCED: Optional[str] = None

def set_dialect_for_tests(name: Optional[str]) -> None:
    global _FORCED
    _FORCED = name.lower() if name else None

def _from_engine_name(name: str) -> Dialect:
    n = name.lower()
    if "sqlite" in n or n in ("file", "memory"):
        return SQLiteDialect()
    if "mysql" in n or "mariadb" in n:
        return MySQLDialect()
    # Default safely to SQLite
    return SQLiteDialect()

def get_dialect() -> Dialect:
    # 1) explicit override
    if _FORCED:
        return _from_engine_name(_FORCED)

    # 2) try to infer from engine object
    eng = get_engine()

    # Common things to inspect (works with many wrappers):
    # - eng.url or eng.database_url or eng.dsn
    # - eng.driver or eng.name or eng.backend
    cand = None
    for attr in ("dialect_name", "name", "driver", "backend"):
        v = getattr(eng, attr, None)
        if isinstance(v, str) and v.strip():
            cand = v
            break

    # Try URL/DSN second
    if cand is None:
        for attr in ("url", "database_url", "dsn"):
            v = getattr(eng, attr, None)
            if isinstance(v, str) and v.strip():
                cand = v
                break

    if not cand:
        # Final fallback
        return SQLiteDialect()

    return _from_engine_name(str(cand))
