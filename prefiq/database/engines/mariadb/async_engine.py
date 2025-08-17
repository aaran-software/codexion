import time
from contextlib import asynccontextmanager, suppress
from typing import Optional, Any, Sequence

from prefiq.database.engines.abstract_engine import AbstractEngine
from prefiq.database.engines.mariadb.logger import log_query
from prefiq.database.engines.mariadb.pool import get_connection, close_pool, _run_in_thread
from prefiq.database.engines.mariadb.retry import with_retry_async


class AsyncMariaDBEngine(AbstractEngine[Any]):
    """
    Asynchronous MariaDB engine.
    Executes queries through connection pool with retry, logging, and lifecycle hooks.
    All blocking driver calls are offloaded to a thread.
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

    # Transaction helpers issue SQL statements via the pooled cursor.
    async def begin(self) -> None:
        async def action():
            async with get_connection(autocommit=False) as cur:
                await _run_in_thread(cur.execute, "START TRANSACTION")
        await with_retry_async(action)

    async def commit(self) -> None:
        async def action():
            async with get_connection(autocommit=False) as cur:
                await _run_in_thread(cur.execute, "COMMIT")
        await with_retry_async(action)

    async def rollback(self) -> None:
        async def action():
            async with get_connection(autocommit=False) as cur:
                await _run_in_thread(cur.execute, "ROLLBACK")
        await with_retry_async(action)

    async def execute(self, query: str, params: Optional[tuple] = None) -> None:
        """Run a non-returning query (INSERT/UPDATE/DELETE)."""
        self._run_hooks('before', query, params)
        start_time = time.time()

        async def action():
            async with get_connection() as cur:
                await _run_in_thread(cur.execute, query, *(params or ()))
                # Commit after write (safe even if autocommit is on)
                if getattr(cur, "connection", None):
                    await _run_in_thread(cur.connection.commit)

        await with_retry_async(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)

    async def fetchone(self, query: str, params: Optional[tuple] = None) -> Any:
        """Run SELECT and return the first row."""
        self._run_hooks('before', query, params)
        start_time = time.time()

        async def action():
            async with get_connection() as cur:
                await _run_in_thread(cur.execute, query, *(params or ()))
                row = await _run_in_thread(cur.fetchone)
                return row

        result = await with_retry_async(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)
        return result

    async def fetchall(self, query: str, params: Optional[tuple] = None) -> list[Any]:
        """Run SELECT and return all rows."""
        self._run_hooks('before', query, params)
        start_time = time.time()

        async def action():
            async with get_connection() as cur:
                await _run_in_thread(cur.execute, query, *(params or ()))
                rows = await _run_in_thread(cur.fetchall)
                return rows

        result = await with_retry_async(action)
        log_query(query, start_time)
        self._run_hooks('after', query, params)
        return result

    async def executemany(self, query: str, param_list: Sequence[tuple]) -> None:
        """Run bulk INSERT/UPDATE with many parameters."""
        self._run_hooks('before', query)
        start_time = time.time()

        async def action():
            async with get_connection() as cur:
                await _run_in_thread(cur.executemany, query, param_list)
                if getattr(cur, "connection", None):
                    await _run_in_thread(cur.connection.commit)

        await with_retry_async(action)
        log_query(query, start_time)
        self._run_hooks('after', query)

    @asynccontextmanager
    async def transaction(self):
        """
        Pin one pooled connection for a multi-statement transaction.
        Usage:
            async with db.transaction() as cur:
                await _run_in_thread(cur.execute, "INSERT ...")
                await _run_in_thread(cur.execute, "UPDATE ...")
        """
        async with get_connection(autocommit=False) as cur:
            # BEGIN with retry
            await with_retry_async(lambda: _run_in_thread(cur.execute, "START TRANSACTION"))
            try:
                yield cur
                # COMMIT with retry
                await with_retry_async(lambda: _run_in_thread(cur.execute, "COMMIT"))
            except Exception:
                # ROLLBACK with retry (best-effort)
                with suppress(Exception):
                    await with_retry_async(lambda: _run_in_thread(cur.execute, "ROLLBACK"))
                raise

    async def test_connection(self) -> bool:
        """Simple connectivity check."""
        try:
            async def action():
                async with get_connection() as cur:
                    await _run_in_thread(cur.execute, "SELECT 1")
                    row = await _run_in_thread(cur.fetchone)
                    return row is not None

            return bool(await with_retry_async(action))
        except Exception:
            return False
