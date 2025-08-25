# prefiq/database/connection.py

from __future__ import annotations

import asyncio
import inspect
import os
from contextlib import contextmanager
from typing import Optional, Any, Dict

from prefiq.settings.get_settings import load_settings, clear_settings_cache

# -------- existing default singleton (backwards compatible) ------------------

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


def _create_engine_for(engine: str, mode: str) -> Any:
    """
    Construct an engine instance for a specific (engine, mode) pair without
    consulting Settings again.
    """
    eng = _normalize(engine)
    if eng == "mariadb":
        if _is_async(mode):
            from prefiq.database.engines.mariadb.async_engine import AsyncMariaDBEngine
            return AsyncMariaDBEngine()
        from prefiq.database.engines.mariadb.sync_engine import SyncMariaDBEngine
        return SyncMariaDBEngine()
    if eng == "postgres":
        if _is_async(mode):
            from prefiq.database.engines.postgres.async_engine import AsyncPostgresEngine
            return AsyncPostgresEngine()
        from prefiq.database.engines.postgres.sync_engine import SyncPostgresEngine
        return SyncPostgresEngine()
    if eng == "sqlite":
        from prefiq.database.engines.sqlite.sync_engine import SQLiteEngine
        return SQLiteEngine()
    raise RuntimeError(f"Unsupported DB engine {engine!r}")


def _make_engine() -> Any:
    """
    Existing behavior: read active Settings and build a single engine.
    """
    s = load_settings()
    eng = _normalize(getattr(s, "DB_ENGINE", None))
    mode = getattr(s, "DB_MODE", "sync")
    return _create_engine_for(eng, mode)


def get_engine() -> Any:
    """
    Return the global DB engine (singleton). Constructed lazily from .env.
    """
    global _engine_singleton
    if _engine_singleton is None:
        _engine_singleton = _make_engine()
    return _engine_singleton


def _close_safely(obj: Any) -> None:
    if not obj or not hasattr(obj, "close"):
        return
    try:
        res = obj.close()
        if inspect.isawaitable(res):
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                asyncio.run(res)
            else:
                asyncio.create_task(res)
    except Exception:
        pass


def reset_engine() -> None:
    """
    Drop the cached engine instance. Any open connections will be closed best-effort.
    """
    global _engine_singleton
    _close_safely(_engine_singleton)
    _engine_singleton = None


def reload_engine_from_env(*, force_refresh: bool = True) -> Any:
    """
    Re-read .env (if changed) and rebuild the default engine singleton.
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
    Programmatic “hot-swap” for the default engine (legacy convenience).
    """
    os.environ["DB_ENGINE"] = engine
    if mode is not None:
        os.environ["DB_MODE"] = mode
    return reload_engine_from_env(force_refresh=True)


# -------- NEW: named engines that can coexist side-by-side -------------------

# Registry of named engines (e.g., "DEV", "PRIMARY", "ANALYTICS")
_named_engines: Dict[str, Any] = {}
_ENV_KEYS = ("DB_ENGINE", "DB_MODE", "DB_HOST", "DB_PORT", "DB_USER", "DB_PASS", "DB_NAME", "DB_POOL_WARMUP")


def _read_named_env(name: str) -> Dict[str, str]:
    """
    Read variables like DEV_DB_HOST, ANALYTICS_DB_NAME, etc., and map them to
    base keys (DB_HOST, DB_NAME, ...). Missing keys are omitted.
    """
    pref = name.upper()
    out: Dict[str, str] = {}
    for k in _ENV_KEYS:
        v = os.getenv(f"{pref}_{k}")
        if v is not None:
            out[k] = v
    return out


@contextmanager
def engine_env(name: str):
    """
    Temporarily patch process env with this engine's (name_) variables mapped to
    base DB_* names — and refresh Settings on enter/exit.

    NOTE: This is scoped and intended for *short* critical sections (e.g.,
    during connection establishment or a transaction). Avoid overlap across
    threads.
    """
    overrides = _read_named_env(name)
    if not overrides:
        # No overrides for this name: act as a no-op
        yield
        return

    # Save prior values to restore later
    prior: Dict[str, Optional[str]] = {k: os.getenv(k) for k in overrides.keys()}
    try:
        for k, v in overrides.items():
            os.environ[k] = v
        clear_settings_cache()
        yield
    finally:
        # restore
        for k, old in prior.items():
            if old is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = old
        clear_settings_cache()


def get_engine_named(name: str) -> Any:
    """
    Return a dedicated engine instance keyed by `name`.
    Requires <NAME>_DB_ENGINE (e.g., DEV_DB_ENGINE, ANALYTICS_DB_ENGINE) in .env.
    """
    key = name.strip()
    if not key:
        raise ValueError("Engine name cannot be empty.")

    if key in _named_engines:
        return _named_engines[key]

    overrides = _read_named_env(key)
    if "DB_ENGINE" not in overrides:
        raise RuntimeError(
            f"No engine configured for {key!r}. Set {key.upper()}_DB_ENGINE and friends in your .env."
        )
    engine_name = overrides.get("DB_ENGINE", "sqlite")
    mode_name = overrides.get("DB_MODE", "sync")

    # Build the engine while the overrides are active, so any engine that reads
    # Settings/env during connect/pool creation sees the right config.
    with engine_env(key):
        eng = _create_engine_for(engine_name, mode_name)
        # Try to establish/prime immediately for sync engines so the connection captures
        # the intended config right now (engines that lazy-connect will still be OK as
        # ConnectionManager wraps operations in engine_env()).
        try:
            if hasattr(eng, "connect") and not _is_async(mode_name):
                eng.connect()  # type: ignore[call-arg]
        except Exception:
            # Let the caller handle connection failures later if needed
            pass

    _named_engines[key] = eng
    return eng


def reset_engine_named(name: str) -> None:
    eng = _named_engines.pop(name, None)
    _close_safely(eng)


def swap_engine_named(name: str, engine: str, *, mode: str | None = None) -> Any:
    """
    Programmatic hot-swap of a *named* engine. Updates process env for that name
    (e.g., DEV_DB_ENGINE=..., DEV_DB_MODE=...) and rebuilds the named engine.
    """
    pref = name.upper()
    os.environ[f"{pref}_DB_ENGINE"] = engine
    if mode is not None:
        os.environ[f"{pref}_DB_MODE"] = mode
    reset_engine_named(name)
    return get_engine_named(name)
