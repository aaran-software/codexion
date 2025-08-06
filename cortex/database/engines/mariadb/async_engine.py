# =============================================================
# AsyncMariaDBEngine (async_engine.py)
#
# Author: Sundar
# Created: 2025-08-06
#
# Purpose:
#   - Asynchronous MariaDB engine implementation.
#   - Uses async pool and dynamic config per request.
#   - Supports hooks, retries, and slow query logging.
#
# Notes for Developers:
#   - Depends on external `init_pool()` at startup.
#   - Use `override_async_config()` for request-scoped overrides.
# =============================================================

import time
from typing import Optional, Any, Coroutine

from cortex.database.engines.abstract_engine import AbstractEngine  # Interface + hooks
from cortex.database.engines.mariadb.logger import log_query  # Logs timing / slow queries
from cortex.database.engines.mariadb.pool import get_connection  # Async context-managed connection
from cortex.database.engines.mariadb.retry import with_retry  # Async retry decorator


class AsyncMariaDBEngine(AbstractEngine):
    """
    Asynchronous MariaDB engine.
    Executes queries through connection pool with retry, logging, and lifecycle hooks.
    """
    def __init__(self):
        super().__init__()  # Set up hook infrastructure

    async def connect(self) -> None:
        # Connection pooling is handled externally (via init_pool). Nothing to do here.
        pass

    async def close(self) -> None:
        # Clean up the global connection pool
        from .pool import close_pool
        await close_pool()

    async def begin(self) -> None:  # <-- IMPROVE: Implement transaction start
        async for cur in get_connection():
            await cur.connection.begin()

    async def commit(self) -> None:  # <-- IMPROVE: Implement properly
        async for cur in get_connection():
            await cur.connection.commit()

    async def rollback(self) -> None:  # <-- IMPROVE: Implement properly
        async for cur in get_connection():
            await cur.connection.rollback()

    async def execute(self, query: str, params: Optional[tuple] = None) -> None:
        # Run non-returning query (e.g., INSERT, UPDATE)
        self._run_hooks('before', query, params)
        start_time = time.time()

        async def action():
            async for cur in get_connection():
                await cur.execute(query, params or ())
                await cur.connection.commit()

        await with_retry(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)

    async def fetchone(self, query: str, params: Optional[tuple] = None):
        # Run SELECT and return first row
        self._run_hooks('before', query, params)
        start_time = time.time()

        async def action():
            async for cur in get_connection():
                await cur.execute(query, params or ())
                return await cur.fetchone()

        result = await with_retry(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)
        return result

    async def fetchall(self, query: str, params: Optional[tuple] = None):
        # Run SELECT and return all rows
        self._run_hooks('before', query, params)
        start_time = time.time()

        async def action():
            async for cur in get_connection():
                await cur.execute(query, params or ())
                return await cur.fetchall()

        result = await with_retry(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)
        return result

    async def executemany(self, query: str, param_list):
        # Run batch operation (bulk INSERT/UPDATE)
        self._run_hooks('before', query)

        async def action():
            async for cur in get_connection():
                await cur.executemany(query, param_list)
                await cur.connection.commit()

        await with_retry(action)
        self._run_hooks('after', query)

    async def test_connection(self) -> bool | None | Any:
        # Check if database is reachable by running a test query
        try:
            async for cur in get_connection():
                await cur.execute("SELECT 1")
                result = await cur.fetchone()
                return result is not None
        except:
            return False
