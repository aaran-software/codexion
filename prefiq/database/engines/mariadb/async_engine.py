# prefiq/database/engines/mariadb/async_engine.py

import time
from typing import Optional, Any

from prefiq.database.engines.abstract_engine import AbstractEngine
from prefiq.database.engines.mariadb.logger import log_query
from prefiq.database.engines.mariadb.pool import get_connection, close_pool
from prefiq.database.engines.mariadb.retry import with_retry


class AsyncMariaDBEngine(AbstractEngine):
    """
    Asynchronous MariaDB engine.
    Executes queries through connection pool with retry, logging, and lifecycle hooks.
    """

    def __init__(self):
        super().__init__()

    async def connect(self) -> None:
        """
        No-op since we rely on connection pool initialization.
        The pool should be started via init_pool() elsewhere.
        """
        return None

    async def close(self) -> None:
        """Close the global async pool."""
        await close_pool()

    async def begin(self) -> None:
        """Start a transaction (disable autocommit)."""
        async with get_connection() as conn:
            await conn.begin()

    async def commit(self) -> None:
        """Commit the current transaction."""
        async with get_connection() as conn:
            await conn.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        async with get_connection() as conn:
            await conn.rollback()

    async def execute(self, query: str, params: Optional[tuple] = None) -> None:
        """Run a non-returning query (INSERT/UPDATE/DELETE)."""
        self._run_hooks('before', query, params)
        start_time = time.time()

        async def action():
            async with get_connection() as cur:
                await cur.execute(query, params or ())
                await cur.connection.commit()

        await with_retry(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)

    async def fetchone(self, query: str, params: Optional[tuple] = None) -> Any:
        """Run SELECT and return the first row."""
        self._run_hooks('before', query, params)
        start_time = time.time()

        async def action():
            async with get_connection() as cur:
                await cur.execute(query, params or ())
                return await cur.fetchone()

        result = await with_retry(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)
        return result

    async def fetchall(self, query: str, params: Optional[tuple] = None) -> list[Any]:
        """Run SELECT and return all rows."""
        self._run_hooks('before', query, params)
        start_time = time.time()

        async def action():
            async with get_connection() as cur:
                await cur.execute(query, params or ())
                return await cur.fetchall()

        result = await with_retry(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)
        return result

    async def executemany(self, query: str, param_list) -> None:
        """Run bulk INSERT/UPDATE with many parameters."""
        self._run_hooks('before', query)

        async def action():
            async with get_connection() as cur:
                await cur.executemany(query, param_list)
                await cur.connection.commit()

        await with_retry(action)
        self._run_hooks('after', query)

    async def test_connection(self) -> bool:
        """Simple connectivity check."""
        try:
            async with get_connection() as cur:
                await cur.execute("SELECT 1")
                result = await cur.fetchone()
                return result is not None
        except Exception:
            return False
