# prefiq/database/connection.py
from __future__ import annotations

from typing import Optional
from prefiq.settings.get_settings import load_settings

# NOTE: these imports assume you actually have these engine classes.
# If you don't, see the "Missing files" section below.
from prefiq.database.engines.mariadb.sync_engine import SyncMariaDBEngine
from prefiq.database.engines.mariadb.async_engine import AsyncMariaDBEngine
from prefiq.database.engines.mysql.sync_engine import SyncMysqlEngine
from prefiq.database.engines.mysql.async_engine import AsyncMysqlEngine
from prefiq.database.engines.sqlite.sqlite_engine import SQLiteEngine

_engine_singleton: Optional[object] = None  # lazy singleton


def _is_async(mode: str) -> bool:
    return (mode or "").lower() == "async"


def _normalize_engine_name(name: str) -> str:
    n = (name or "").lower()
    # allow aliases; expand later if you add more engines
    aliases = {"postgresql": "postgres", "sqlite3": "sqlite"}
    return aliases.get(n, n)


def _make_engine():
    s = load_settings()
    eng = _normalize_engine_name(getattr(s, "DB_ENGINE", ""))

    if eng == "mariadb":
        return AsyncMariaDBEngine() if _is_async(s.DB_MODE) else SyncMariaDBEngine()

    if eng == "mysql":
        return AsyncMysqlEngine() if _is_async(s.DB_MODE) else SyncMysqlEngine()

    if eng == "sqlite":
        # single (sync) engine in this stack
        return SQLiteEngine()

    # If you add postgres etc., map them here before enabling in error text
    raise RuntimeError(
        f"Unsupported DB_ENGINE '{s.DB_ENGINE}'. "
        "Use one of: mariadb, mysql, sqlite."
    )


def get_engine():
    """
    Return the process‑wide DB engine instance (lazy singleton).
    """
    global _engine_singleton
    if _engine_singleton is None:
        _engine_singleton = _make_engine()
    return _engine_singleton


def reset_engine():
    """
    Drop the cached engine. Useful in tests when env changes or you need a fresh pool.
    """
    global _engine_singleton
    if _engine_singleton and hasattr(_engine_singleton, "close"):
        try:
            _engine_singleton.close()
        except Exception:
            pass
    _engine_singleton = None
