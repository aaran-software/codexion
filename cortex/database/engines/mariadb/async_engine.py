import time
from typing import Optional
from .abstract import AbstractEngine
from .retry import with_retry
from .logger import log_query
from .pool import get_connection

class AsyncMariaDBEngine(AbstractEngine):
    def __init__(self):
        super().__init__()

    async def connect(self) -> None:
        pass  # already handled via init_pool externally

    async def close(self) -> None:
        from .pool import close_pool
        await close_pool()

    async def begin(self) -> None:
        pass  # not needed unless doing transactions manually

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    async def execute(self, query: str, params: Optional[tuple] = None) -> None:
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
        self._run_hooks('before', query)

        async def action():
            async for cur in get_connection():
                await cur.executemany(query, param_list)
                await cur.connection.commit()

        await with_retry(action)
        self._run_hooks('after', query)

    async def test_connection(self) -> bool:
        try:
            async for cur in get_connection():
                await cur.execute("SELECT 1")
                result = await cur.fetchone()
                return result is not None
        except:
            return False