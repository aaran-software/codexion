from __future__ import annotations

import asyncio
from typing import Any, Optional, Sequence, Tuple, Dict

from prefiq.settings.get_settings import load_settings

try:
    import asyncpg  # pip install asyncpg
except Exception as e:  # pragma: no cover
    asyncpg = None
    _IMPORT_ERR = e
else:
    _IMPORT_ERR = None


class AsyncPostgresEngine:
    """
    Minimal async Postgres engine built on asyncpg.
    Matches the call surface used elsewhere: execute(), fetchone(), fetchall(), close().

    IMPORTANT: We pass connection parameters (host/port/user/password/database)
    instead of a DSN string so special characters in credentials (like '@') do not
    corrupt parsing.
    """

    dialect_name = "postgres"
    name = "postgres"
    driver = "asyncpg"

    def __init__(self) -> None:
        if asyncpg is None:
            raise RuntimeError(
                "asyncpg is required for AsyncPostgresEngine. "
                f"Original import error: {_IMPORT_ERR!r}"
            )
        s = load_settings()
        host = (getattr(s, "DB_HOST", "localhost") or "").strip()
        port = int(getattr(s, "DB_PORT", 5432))
        user = getattr(s, "DB_USER", "postgres")
        password = getattr(s, "DB_PASS", "")
        database = getattr(s, "DB_NAME", "postgres")

        # Store connection params for create_pool()
        self._params: Dict[str, Any] = dict(
            host=host, port=port, user=user, password=password, database=database
        )

        # Human-friendly URL for doctor logs (password masked)
        self.url = f"postgresql://{user}:*****@{host}:{port}/{database}"

        self._pool: Optional[asyncpg.Pool] = None

    # ---------- internals ----------

    async def _ensure_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            warm = max(1, int(getattr(load_settings(), "DB_POOL_WARMUP", 1)))
            self._pool = await asyncpg.create_pool(min_size=1, max_size=warm, **self._params)
        return self._pool

    @staticmethod
    def _row_to_tuple(row: Any) -> Tuple[Any, ...]:
        # asyncpg.Record → tuple
        if row is None:
            return ()
        try:
            return tuple(row.values())
        except Exception:
            return tuple(row)

    # ---------- public API (async) ----------

    async def aexecute(self, sql: str, params: Sequence[Any] | None = None) -> Any:
        pool = await self._ensure_pool()
        async with pool.acquire() as conn:
            return await conn.execute(sql, *(params or ()))

    async def afetchone(self, sql: str, params: Sequence[Any] | None = None) -> Optional[Tuple[Any, ...]]:
        pool = await self._ensure_pool()
        async with pool.acquire() as conn:
            rec = await conn.fetchrow(sql, *(params or ()))
            return self._row_to_tuple(rec) if rec is not None else None

    async def afetchall(self, sql: str, params: Sequence[Any] | None = None) -> list[Tuple[Any, ...]]:
        pool = await self._ensure_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *(params or ()))
            return [self._row_to_tuple(r) for r in rows]

    async def aclose(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    # ---------- sync facade (for callers that don't await) ----------

    def _run(self, coro):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro)
        # If a loop is already running in this thread,
        # use it to run the coroutine to completion.
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)  # type: ignore[call-arg]

    # Synchronous wrappers expected by queries/builder:
    def execute(self, sql: str, params: Sequence[Any] | None = None) -> Any:
        return self._run(self.aexecute(sql, params))

    def fetchone(self, sql: str, params: Sequence[Any] | None = None) -> Optional[Tuple[Any, ...]]:
        return self._run(self.afetchone(sql, params))

    def fetchall(self, sql: str, params: Sequence[Any] | None = None) -> list[Tuple[Any, ...]]:
        return self._run(self.afetchall(sql, params))

    def close(self) -> None:
        try:
            self._run(self.aclose())
        except Exception:
            pass
