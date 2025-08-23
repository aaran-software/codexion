# prefiq/database/connection.py
from __future__ import annotations

import os
from typing import Optional, Any

from prefiq.settings.get_settings import load_settings, clear_settings_cache

# Engines we actually support right now
from prefiq.database.engines.mariadb.sync_engine import SyncMariaDBEngine
from prefiq.database.engines.mariadb.async_engine import AsyncMariaDBEngine
from prefiq.database.engines.sqlite.sync_engine import SQLiteEngine

_engine_singleton: Optional[Any] = None  # lazy, process-wide


def _is_async(mode: str | None) -> bool:
    return (mode or "").strip().lower() == "async"


def _normalize(name: str | None) -> str:
    n = (name or "").strip().lower()
    aliases = {"sqlite3": "sqlite", "postgresql": "postgres"}  # future-friendly
    return aliases.get(n, n)


def _make_engine() -> Any:
    s = load_settings()
    eng = _normalize(getattr(s, "DB_ENGINE", None))
    mode = getattr(s, "DB_MODE", "sync")

    if eng == "mariadb":
        return AsyncMariaDBEngine() if _is_async(mode) else SyncMariaDBEngine()

    if eng == "sqlite":
        # SQLite stack is sync-only (for now)
        return SQLiteEngine()

    raise RuntimeError(
        f"Unsupported DB_ENGINE {getattr(s, 'DB_ENGINE', None)!r}. "
        "Use one of: mariadb, sqlite."
    )


def get_engine() -> Any:
    """
    Return the global DB engine (singleton). Constructed lazily from .env.
    """
    global _engine_singleton
    if _engine_singleton is None:
        _engine_singleton = _make_engine()
    return _engine_singleton


def reset_engine() -> None:
    """
    Drop the cached engine instance. Any open connections will be closed best-effort.
    """
    global _engine_singleton
    eng = _engine_singleton
    if eng and hasattr(eng, "close"):
        try:
            eng.close()  # sync engines; async engines expose close() coroutine in our stack as well
        except Exception:
            pass
    _engine_singleton = None


def reload_engine_from_env(*, force_refresh: bool = True) -> Any:
    """
    Re-read .env (if changed) and rebuild the engine singleton.

    Typical usage:
        os.environ["DB_ENGINE"] = "sqlite"
        reload_engine_from_env()
    """
    if force_refresh:
        clear_settings_cache()
    reset_engine()
    return get_engine()


def swap_engine(engine: str, *, mode: str | None = None) -> Any:
    """
    Programmatic “hot-swap” (handy in tests or dev tools).
    This writes into process env, clears settings cache, and rebuilds the engine.

    swap_engine("sqlite")
    swap_engine("mariadb", mode="async")
    """
    os.environ["DB_ENGINE"] = engine
    if mode is not None:
        os.environ["DB_MODE"] = mode
    return reload_engine_from_env(force_refresh=True)
