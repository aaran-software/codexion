# =============================================================
# MariaDB Connection Pool (pool.py)
#
# Author: ChatGPT (refactored for dynamic configuration)
# Created: 2025-08-06
#
# Purpose:
#   - Provide async-compatible MariaDB connection via context manager.
#   - Designed to work with thread-local dynamic config loader.
#
# Notes for Developers:
#   - This is not a real persistent pool, but a thin wrapper that opens a new
#     thread-based connection per request and closes it automatically.
#   - To override the dynamic config (from thread-local), use `init_pool()`.
#   - Recommended for async apps needing short-lived, isolated DB operations.
# =============================================================

import mariadb
from contextlib import asynccontextmanager
from anyio.to_thread import run_sync
from cortex.database.config_loader.base import use_thread_config

# Optional override for global pool config, else dynamic config is used
_pool_config = None

def init_pool(config: dict):
    """
    Set a static configuration globally (e.g., in startup).
    Will override the thread-local config temporarily.
    """
    global _pool_config
    _pool_config = config


@asynccontextmanager
async def get_connection():
    """
    Async context manager that yields a MariaDB cursor.
    - Acquires connection using thread-local or global config
    - Commits and closes connection after use
    - Use inside `async with` blocks
    """
    config = _pool_config or use_thread_config().get_config_dict()

    def create_connection_and_cursor():
        connection = mariadb.connect(**config)
        cursor = connection.cursor()
        return connection, cursor

    db_conn, db_cursor = await run_sync(create_connection_and_cursor)
    try:
        yield db_cursor
        await run_sync(db_conn.commit)
    finally:
        await run_sync(db_cursor.close)
        await run_sync(db_conn.close)


async def close_pool():
    """
    No-op placeholder for API symmetry. Required only if a real async pool is used.
    """
    pass