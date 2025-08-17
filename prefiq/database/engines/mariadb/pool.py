# =============================================================
# MariaDB Connection Pool (pool.py) - Pure Python
# =============================================================

import asyncio
import time
from contextlib import asynccontextmanager
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, ParamSpec, Mapping

import mariadb

from prefiq.database.config_loader.base import use_thread_config

T = TypeVar("T")
P = ParamSpec("P")

# Pool management
_pool_config: Optional[Dict[str, Any]] = None
_connection_pool: List[mariadb.Connection] = []
_connection_times: Dict[mariadb.Connection, float] = {}
_pool_lock = asyncio.Lock()


def init_pool(config: Dict[str, Any]) -> None:
    """
    Initialize connection pool with configuration.

    Args:
        config: Dictionary containing:
            - max_lifetime: Maximum connection lifetime in seconds (default: 3600)
            - pool_size: Maximum pool size (default: 10)
            - Standard MariaDB connection parameters
    """
    global _pool_config
    _pool_config = {
        **config,
        "max_lifetime": config.get("max_lifetime", 3600.0),  # ensure numeric defaults
        "pool_size": config.get("pool_size", 10),
    }


# ---------- typing-safe thread runner ----------

def _apply(func: Callable[P, T], args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> T:
    """Adapter executed inside the worker thread."""
    return func(*args, **kwargs)

async def _run_in_thread(func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs) -> T:
    """
    Run a blocking function in a thread, with precise typing that satisfies type checkers.
    We pass an adapter (_apply) to run_in_executor, along with func, args, kwargs.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _apply, func, tuple(args), dict(kwargs))


# ---------- small helpers to keep type-checkers happy ----------

def _cfg_float(cfg: Mapping[str, Any], key: str, default: float) -> float:
    """Get a float from cfg[key], falling back to default; robust for strings/ints."""
    val = cfg.get(key, default)
    try:
        if val is None:
            return float(default)
        return float(val)
    except (TypeError, ValueError):
        return float(default)

def _cfg_int(cfg: Mapping[str, Any], key: str, default: int) -> int:
    """Get an int from cfg[key], falling back to default; robust for strings/floats."""
    val = cfg.get(key, default)
    try:
        if val is None:
            return int(default)
        return int(val)
    except (TypeError, ValueError):
        return int(default)


async def _clean_expired_connections() -> None:
    """Remove expired or broken connections from the pool."""
    if _pool_config is None:
        return

    async with _pool_lock:
        now = time.time()
        max_lifetime = _cfg_float(_pool_config, "max_lifetime", 3600.0)

        valid: List[mariadb.Connection] = []
        for conn in _connection_pool:
            created_at = _connection_times.get(conn, 0.0)
            if now - created_at < max_lifetime:
                try:
                    await _run_in_thread(conn.ping)
                    valid.append(conn)
                except mariadb.Error:
                    await _run_in_thread(conn.close)
            else:
                await _run_in_thread(conn.close)

        _connection_pool[:] = valid
        _connection_times.clear()
        _connection_times.update({c: now for c in valid})


async def _get_connection() -> mariadb.Connection:
    """Get a connection from pool or create new one."""
    await _clean_expired_connections()
    if _pool_config is None:
        # Initialize from the active (thread/async-local) config if not set yet
        config = use_thread_config().get_config_dict()
        init_pool(config)

    cfg = _pool_config  # local alias for type-checkers
    assert cfg is not None

    async with _pool_lock:
        # Try to get connection from pool
        while _connection_pool:
            conn = _connection_pool.pop()
            try:
                await _run_in_thread(conn.ping)
                return conn
            except mariadb.Error:
                await _run_in_thread(conn.close)

        # Create new connection if pool is empty
        config = {k: v for k, v in cfg.items() if k not in ("max_lifetime", "pool_size")}
        return await _run_in_thread(mariadb.connect, **config)


async def _return_connection(conn: mariadb.Connection) -> None:
    """Return connection to the pool, or close it if pool is full or dead."""
    cfg = _pool_config
    assert cfg is not None

    async with _pool_lock:
        try:
            await _run_in_thread(conn.ping)
            pool_size = _cfg_int(cfg, "pool_size", 10)
            if len(_connection_pool) < pool_size:
                _connection_pool.append(conn)
                _connection_times[conn] = time.time()
            else:
                await _run_in_thread(conn.close)
        except mariadb.Error:
            await _run_in_thread(conn.close)


@asynccontextmanager
async def get_connection(autocommit: bool = True):
    """
    Async context manager for MariaDB connections with pooling.

    Usage:
        async with get_connection() as cursor:
            # All cursor/connection methods are blocking; use _run_in_thread on them
            await _run_in_thread(cursor.execute, "SELECT 1")
    """
    if _pool_config is None:
        config = use_thread_config().get_config_dict()
        init_pool(config)

    conn = await _get_connection()
    try:
        cursor = await _run_in_thread(conn.cursor)
        try:
            yield cursor
            # Commit at the end of the context (autocommit-like)
            if autocommit:
                await _run_in_thread(conn.commit)
        finally:
            await _run_in_thread(cursor.close)
            await _return_connection(conn)
    except Exception:
        # If anything goes wrong, ensure the connection is closed (not returned to pool)
        await _run_in_thread(conn.close)
        raise

async def prewarm(count: int = 1) -> None:
    """
    Proactively open `count` connections and return them to the pool.
    Useful at boot so the first query doesn't pay init cost.
    """
    if count <= 0:
        return

    # ensure pool is initialized (re-using your current init-on-demand)
    if _pool_config is None:
        config = use_thread_config().get_config_dict()
        init_pool(config)

    # open connections, then put them back
    conns: list[mariadb.Connection] = []
    try:
        for _ in range(count):
            conns.append(await _get_connection())
    finally:
        for c in conns:
            # pretend we used the conn; just return to pool
            await _return_connection(c)


async def close_pool() -> None:
    """Close all pooled connections and clear state."""
    async with _pool_lock:
        for conn in _connection_pool:
            try:
                await _run_in_thread(conn.close)
            except mariadb.Error:
                pass
        _connection_pool.clear()
        _connection_times.clear()
