# =============================================================
# AsyncSQLiteEngine
# file path: prefiq/database/engines/sqlite/async_engine.py
#
# Author: Sundar
# Created: 2025-08-18
#
# Purpose:
#   - Asynchronous SQLite engine with an API paralleling AbstractEngine,
#     but using async methods (does not subclass AbstractEngine).
#   - Hook-aware (before/after), PRAGMAs applied on connect.
# =============================================================

from __future__ import annotations

import os
import time
from typing import Any, Optional, Sequence, List
from contextlib import asynccontextmanager

from prefiq.database.config_loader.base import use_thread_config
from prefiq.log.logger import get_logger

LOG = get_logger("prefiq.database.sqlite.async")

try:
    import aiosqlite  # type: ignore
except Exception:  # pragma: no cover
    aiosqlite = None

_DEFAULT_PATH = os.path.join(".prefiq", "devmeta.sqlite")


def _resolve_sqlite_path() -> str:
    cfg = {}
    try:
        cfg = use_thread_config().get_config_dict() or {}
    except Exception:
        pass

    for key in ("path", "database", "filename"):
        val = cfg.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return _DEFAULT_PATH


async def _apply_pragmas(conn: "aiosqlite.Connection") -> None:  # type: ignore[name-defined]
    await conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        PRAGMA foreign_keys=ON;
        PRAGMA synchronous=NORMAL;
        PRAGMA temp_store=MEMORY;
        """
    )


class AsyncSQLiteEngine:
    """
    Async SQLite engine with an API similar to AbstractEngine, using async methods.

    Methods:
        await connect(), await close()
        await execute(), await executemany()
        await fetchone(), await fetchall()
        async with transaction(): ...
        await begin()/commit()/rollback()
        await test_connection()

    Hooks:
        set_before_execute_hook(func)
        set_after_execute_hook(func)
        (func signature: hook(query: str, params: Optional[tuple], stage: str) -> None)
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        if aiosqlite is None:
            raise RuntimeError("AsyncSQLiteEngine requires 'aiosqlite' to be installed")
        self._db_path = db_path
        self.conn: Optional["aiosqlite.Connection"] = None  # type: ignore[name-defined]
        self.before_execute_hook = None
        self.after_execute_hook = None

    # ---- hooks ----
    def set_before_execute_hook(self, hook): self.before_execute_hook = hook
    def set_after_execute_hook(self, hook): self.after_execute_hook = hook
    def _run_hooks(self, stage: str, query: str, params: Optional[tuple] = None) -> None:
        hook = self.before_execute_hook if stage == "before" else self.after_execute_hook
        if hook:
            hook(query, params, stage)

    # ---- lifecycle ----
    async def connect(self) -> None:
        assert aiosqlite is not None
        path = self._db_path or _resolve_sqlite_path()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.conn = await aiosqlite.connect(path)
        self.conn.row_factory = aiosqlite.Row  # type: ignore[attr-defined]
        await _apply_pragmas(self.conn)

    async def close(self) -> None:
        if self.conn is not None:
            try:
                await self.conn.close()
            finally:
                self.conn = None

    def _ensure_conn(self) -> "aiosqlite.Connection":  # type: ignore[name-defined]
        if self.conn is None:
            raise RuntimeError("AsyncSQLiteEngine is not connected. Call await connect() first.")
        return self.conn

    # ---- transactions ----
    async def begin(self) -> None:
        await self._ensure_conn().execute("BEGIN")

    async def commit(self) -> None:
        await self._ensure_conn().commit()

    async def rollback(self) -> None:
        await self._ensure_conn().rollback()

    @asynccontextmanager
    async def transaction(self):
        conn = self._ensure_conn()
        try:
            await conn.execute("BEGIN")
            yield
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise

    # ---- queries ----
    async def execute(self, query: str, params: Optional[tuple] = None) -> None:
        conn = self._ensure_conn()
        self._run_hooks("before", query, params)
        t0 = time.time()
        await conn.execute(query, params or ())
        await conn.commit()
        self._run_hooks("after", query, params)
        LOG.debug("sqlite_async_execute", extra={"elapsed_ms": int((time.time() - t0) * 1000)})

    async def executemany(self, query: str, param_list: Sequence[tuple]) -> None:
        conn = self._ensure_conn()
        self._run_hooks("before", query, None)
        t0 = time.time()
        await conn.executemany(query, list(param_list))
        await conn.commit()
        self._run_hooks("after", query, None)
        LOG.debug("sqlite_async_executemany", extra={"elapsed_ms": int((time.time() - t0) * 1000)})

    async def fetchone(self, query: str, params: Optional[tuple] = None) -> Optional[Any]:
        conn = self._ensure_conn()
        self._run_hooks("before", query, params)
        t0 = time.time()
        cur = await conn.execute(query, params or ())
        row = await cur.fetchone()
        self._run_hooks("after", query, params)
        LOG.debug("sqlite_async_fetchone", extra={"elapsed_ms": int((time.time() - t0) * 1000)})
        return row

    async def fetchall(self, query: str, params: Optional[tuple] = None) -> List[Any]:
        conn = self._ensure_conn()
        self._run_hooks("before", query, params)
        t0 = time.time()
        cur = await conn.execute(query, params or ())
        rows = await cur.fetchall()
        self._run_hooks("after", query, params)
        LOG.debug("sqlite_async_fetchall", extra={"elapsed_ms": int((time.time() - t0) * 1000)})
        return list(rows)

    # ---- health ----
    async def test_connection(self) -> bool:
        try:
            conn = self._ensure_conn()
            cur = await conn.execute("SELECT 1")
            row = await cur.fetchone()
            return row is not None
        except Exception:
            return False
