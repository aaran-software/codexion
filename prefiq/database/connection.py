# prefiq/database/connection.py
from __future__ import annotations

import asyncio
import inspect
import os
from typing import Optional, Any

from prefiq.settings.get_settings import load_settings, clear_settings_cache

_engine_singleton: Optional[Any] = None  # lazy, process-wide


def _is_async(mode: str | None) -> bool:
    return (mode or "").strip().lower() == "async"


def _normalize(name: str | None) -> str:
    n = (name or "").strip().lower()
    # Map common aliases
    aliases = {
        "sqlite3": "sqlite",
        "postgresql": "postgres",
        "pg": "postgres",
        # If you want MySQL to ride the MariaDB engines, uncomment:
        "mysql": "mariadb",
    }
    return aliases.get(n, n)


def _make_engine() -> Any:
    s = load_settings()
    eng = _normalize(getattr(s, "DB_ENGINE", None))
    mode = getattr(s, "DB_MODE", "sync")

    # --- MariaDB (and optionally MySQL via alias above) ---
    if eng == "mariadb":
        if _is_async(mode):
            from prefiq.database.engines.mariadb.async_engine import AsyncMariaDBEngine
            return AsyncMariaDBEngine()
        from prefiq.database.engines.mariadb.sync_engine import SyncMariaDBEngine
        return SyncMariaDBEngine()

    # --- Postgres ---
    if eng == "postgres":
        if _is_async(mode):
            from prefiq.database.engines.postgres.async_engine import AsyncPostgresEngine
            return AsyncPostgresEngine()
        from prefiq.database.engines.postgres.sync_engine import SyncPostgresEngine
        return SyncPostgresEngine()

    # --- SQLite (sync-only here) ---
    if eng == "sqlite":
        from prefiq.database.engines.sqlite.sync_engine import SQLiteEngine
        return SQLiteEngine()

    raise RuntimeError(
        f"Unsupported DB_ENGINE {getattr(s, 'DB_ENGINE', None)!r}. "
        "Use one of: mariadb, postgres, sqlite."
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
            res = eng.close()
            if inspect.isawaitable(res):
                try:
                    asyncio.get_running_loop()
                except RuntimeError:
                    asyncio.run(res)
                else:
                    asyncio.create_task(res)
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
    swap_engine("postgres", mode="sync")
    """
    os.environ["DB_ENGINE"] = engine
    if mode is not None:
        os.environ["DB_MODE"] = mode
    return reload_engine_from_env(force_refresh=True)
