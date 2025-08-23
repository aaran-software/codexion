# prefiq/database/connection_manager.py
from __future__ import annotations

from contextlib import contextmanager, asynccontextmanager
from typing import Any, Generator, AsyncGenerator

from prefiq.database.connection import get_engine


class ConnectionManager:
    """
    Thin convenience wrapper around the selected engine.

    - Works for both sync and async MariaDB engines and sync SQLite.
    - Uses engine.transaction() if available; otherwise falls back to manual begin/commit.
    """

    # ---- engine access ------------------------------------------------------

    def get_engine(self) -> Any:
        return get_engine()

    def test(self) -> bool:
        """
        Safe health check that returns a bool for both sync/async engines.
        """
        eng = self.get_engine()
        try:
            res = eng.test_connection()
            # For async engines, test_connection() returns an awaitable — treat as unhealthy here.
            # Prefer using the async helper in callers if you want to await it.
            return bool(res)
        except Exception:
            return False

    def close(self) -> None:
        """
        Close connections/pool if the engine exposes close().
        """
        eng = self.get_engine()
        try:
            eng.close()
        except Exception:
            pass

    # ---- sync transactions --------------------------------------------------

    @contextmanager
    def transaction(self) -> Generator[Any, None, None]:
        """
        Synchronous transaction context. If the engine exposes a context-managed
        .transaction(), we delegate to it. Otherwise we emulate with begin/commit/rollback.
        """
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
        except Exception:
            try:
                eng.rollback()
            finally:
                pass
            raise

    # ---- async transactions -------------------------------------------------

    @asynccontextmanager
    async def transaction_async(self) -> AsyncGenerator[Any, None]:
        """
        Asynchronous transaction context for async MariaDB engine.
        For sync engines (e.g., SQLite), this will raise NotImplementedError.
        """
        eng = self.get_engine()

        if not (hasattr(eng, "begin") and hasattr(eng, "commit")):
            raise NotImplementedError("Async transactions not supported by this engine")

        # If engine implements an async context manager, prefer that.
        if hasattr(eng, "transaction"):
            cm = eng.transaction()  # may be async context manager
            if hasattr(cm, "__aenter__"):
                async with cm:  # type: ignore[misc]
                    yield cm  # engine’s CM yields cursor in our MariaDB async impl
                return

        # Manual async flow (begin/commit/rollback are awaitables on async engine)
        try:
            await eng.begin()
            yield eng
            await eng.commit()
        except Exception:
            try:
                await eng.rollback()
            finally:
                pass
            raise


# convenient singleton
connection_manager = ConnectionManager()
