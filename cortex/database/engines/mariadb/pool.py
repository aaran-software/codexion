# =============================================================
# MariaDB Connection Pool (pool.py) - Pure Python
# =============================================================
import mariadb
import time
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Optional, List
from concurrent.futures import ThreadPoolExecutor
from cortex.database.config_loader.base import use_thread_config

# Pool management
_pool_config: Optional[Dict] = None
_connection_pool: List[mariadb.Connection] = []
_connection_times: Dict[mariadb.Connection, float] = {}
_pool_lock = asyncio.Lock()
_executor = ThreadPoolExecutor(max_workers=4)  # For running sync DB operations


def init_pool(config: dict):
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
        'max_lifetime': config.get('max_lifetime', 3600),
        'pool_size': config.get('pool_size', 10)
    }


async def _run_in_thread(func, *args):
    """Run synchronous function in thread pool"""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, func, *args)


async def _clean_expired_connections():
    """Remove expired or broken connections from the pool"""
    async with _pool_lock:
        now = time.time()
        valid = []

        for conn in _connection_pool:
            created_at = _connection_times.get(conn, 0)
            if now - created_at < _pool_config['max_lifetime']:
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
    """Get a connection from pool or create new one"""
    await _clean_expired_connections()

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
        config = {k: v for k, v in _pool_config.items()
                  if k not in ('max_lifetime', 'pool_size')}
        return await _run_in_thread(mariadb.connect, **config)


async def _return_connection(conn: mariadb.Connection):
    """Return connection to the pool, or close it if pool is full or dead"""
    async with _pool_lock:
        try:
            await _run_in_thread(conn.ping)
            if len(_connection_pool) < _pool_config['pool_size']:
                _connection_pool.append(conn)
                _connection_times[conn] = time.time()
            else:
                await _run_in_thread(conn.close)
        except mariadb.Error:
            await _run_in_thread(conn.close)


@asynccontextmanager
async def get_connection():
    """
    Async context manager for MariaDB connections with pooling.

    Usage:
        async with get_connection() as cursor:
            await cursor.execute("SELECT 1")
    """
    if _pool_config is None:
        config = use_thread_config().get_config_dict()
        init_pool(config)

    conn = await _get_connection()
    try:
        cursor = await _run_in_thread(conn.cursor)
        try:
            yield cursor
            await _run_in_thread(conn.commit)
        finally:
            await _run_in_thread(cursor.close)
            await _return_connection(conn)
    except Exception:
        await _run_in_thread(conn.close)
        raise


async def close_pool():
    """Close all pooled connections and clear state"""
    async with _pool_lock:
        for conn in _connection_pool:
            try:
                await _run_in_thread(conn.close)
            except mariadb.Error:
                pass
        _connection_pool.clear()
        _connection_times.clear()