# prefiq/database/engines/postgres/async_engine.py
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

    IMPORTANT:
      * No shared pool — each call opens/closes its own connection.
      * This avoids cross-event-loop issues when sync wrappers call asyncio.run()
        multiple times in the same process (e.g., CLI tools), which can cause
        'another operation is in progress' with pooled connections.
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

        # Store connection params for connect()
        self._params: Dict[str, Any] = dict(
            host=host, port=port, user=user, password=password, database=database
        )

        # Display URL for diagnostics (mask password)
        self.url = f"postgresql://{user}:*****@{host}:{port}/{database}"

    # ---------- internals ----------

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
        conn = await asyncpg.connect(**self._params)
        try:
            return await conn.execute(sql, *(params or ()))
        finally:
            await conn.close()

    async def afetchone(self, sql: str, params: Sequence[Any] | None = None) -> Optional[Tuple[Any, ...]]:
        conn = await asyncpg.connect(**self._params)
        try:
            rec = await conn.fetchrow(sql, *(params or ()))
            return self._row_to_tuple(rec) if rec is not None else None
        finally:
            await conn.close()

    async def afetchall(self, sql: str, params: Sequence[Any] | None = None) -> list[Tuple[Any, ...]]:
        conn = await asyncpg.connect(**self._params)
        try:
            rows = await conn.fetch(sql, *(params or ()))
            return [self._row_to_tuple(r) for r in rows]
        finally:
            await conn.close()

    async def aclose(self) -> None:
        # no shared pool; nothing to close
        return None

    # ---------- sync facade (for callers that don't await) ----------

    def _run(self, coro):
        # If there is *no* running loop, use asyncio.run (simple & safe)
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro)
        # If a loop is already running in this thread, create a new loop
        # in a temporary thread for this call (avoid blocking the running loop)
        from concurrent.futures import ThreadPoolExecutor

        def _runner() -> Any:
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                return loop.run_until_complete(coro)
            finally:
                try:
                    loop.run_until_complete(asyncio.sleep(0))
                except Exception:
                    pass
                loop.close()

        with ThreadPoolExecutor(max_workers=1) as ex:
            fut = ex.submit(_runner)
            return fut.result()

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
