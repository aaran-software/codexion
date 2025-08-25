# prefiq/database/connection_manager.py

from __future__ import annotations

import asyncio
import inspect
from contextlib import contextmanager, asynccontextmanager
from typing import Any, Generator, AsyncGenerator, Optional

from prefiq.database.connection import get_engine, get_engine_named, engine_env


class ConnectionManager:
    """
    Thin convenience wrapper around a chosen engine.

    - Works for both sync and async engines.
    - Uses engine.transaction() if available; otherwise falls back to manual begin/commit.
    - NEW: can be pinned to a *named* engine (e.g., DEV / ANALYTICS) so multiple
      databases can be used concurrently in one process.
    """

    def __init__(self, engine_name: Optional[str] = None) -> None:
        self._engine_name = engine_name

    # ---- engine access ------------------------------------------------------

    def get_engine(self) -> Any:
        if self._engine_name:
            return get_engine_named(self._engine_name)
        return get_engine()

    def test(self) -> bool:
        """
        Safe health check that returns a bool for both sync/async engines.
        """
        eng = self.get_engine()
        try:
            res = eng.test_connection()
            # For async engines, test_connection() may return an awaitable — treat as unhealthy here.
            # Prefer using the async helper in callers if you want to await it.
            return bool(res)
        except (ValueError, TypeError):
            return False

    def close(self) -> None:
        """
        Close connections/pool if the engine exposes close().
        Supports both sync and async engines.
        """
        eng = self.get_engine()
        try:
            if not hasattr(eng, "close"):
                return
            res = eng.close()
            if inspect.isawaitable(res):
                # If we're in a plain CLI/atexit (no running loop), use asyncio.run
                try:
                    asyncio.get_running_loop()
                except RuntimeError:
                    asyncio.run(res)
                else:
                    # If a loop is already running, fire-and-forget is the safest here.
                    asyncio.create_task(res)
        except (ValueError, TypeError):
            pass

    # ---- sync transactions --------------------------------------------------

    @contextmanager
    def transaction(self) -> Generator[Any, None, None]:
        """
        Synchronous transaction context. If the engine exposes a context-managed
        .transaction(), we delegate to it. Otherwise we emulate with begin/commit/rollback.
        """
        # Ensure any engine that consults Settings/env at call time sees the right values
        ctx = engine_env(self._engine_name) if self._engine_name else _NOOP_CONTEXT()
        with ctx:  # type: ignore[misc]
            eng = self.get_engine()

            # Prefer engine-provided context manager
            if hasattr(eng, "transaction"):
                with eng.transaction() as res:  # type: ignore[attr-defined]
                    yield res
                return

            # Fallback to manual flow
            try:
                eng.begin()
                yield eng
                eng.commit()
            except (ValueError, TypeError):
                try:
                    eng.rollback()
                finally:
                    pass
                raise

    # ---- async transactions -------------------------------------------------

    @asynccontextmanager
    async def transaction_async(self) -> AsyncGenerator[Any, None]:
        """
        Asynchronous transaction context for async engines.
        For sync engines (e.g., SQLite), this will raise NotImplementedError.
        """
        ctx = engine_env(self._engine_name) if self._engine_name else _NOOP_ASYNC_CONTEXT()
        async with ctx:  # type: ignore[misc]
            eng = self.get_engine()

            if not (hasattr(eng, "begin") and hasattr(eng, "commit")):
                raise NotImplementedError("Async transactions not supported by this engine")

            # If engine implements an async context manager, prefer that.
            if hasattr(eng, "transaction"):
                cm = eng.transaction()  # may be async CM
                if hasattr(cm, "__aenter__"):
                    async with cm:  # type: ignore[misc]
                        yield cm  # engine’s CM often yields a cursor
                    return

            # Manual async flow (begin/commit/rollback are awaitables on async engine)
            try:
                await eng.begin()
                yield eng
                await eng.commit()
            except (ValueError, TypeError):
                try:
                    await eng.rollback()
                finally:
                    pass
                raise


# --- tiny helpers to keep context-manager logic tidy -------------------------

@contextmanager
def _NOOP_CONTEXT():
    yield


@asynccontextmanager
async def _NOOP_ASYNC_CONTEXT():
    yield


# convenient singletons (backwards-compatible default + examples for named)
connection_manager = ConnectionManager()
dev_connection_manager = ConnectionManager("DEV")
analytics_connection_manager = ConnectionManager("ANALYTICS")
