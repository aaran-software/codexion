# prefiq/database/connection_manager.py
from contextlib import contextmanager, asynccontextmanager
from typing import Optional, Generator, AsyncGenerator

from prefiq.database.connection import get_engine
from prefiq.database.config_loader.base import (
    override_thread_config,
    override_async_config,
    use_thread_config,
    use_async_config,
)


class ConnectionManager:
    """
    Connection Manager
    ------------------
    Central abstraction for managing database connections.
    Works with both sync and async engines transparently.
    """

    def __init__(self, engine=None):
        self._engine = engine or get_engine

    def get_engine(self):
        """Return the active DB engine (sync or async)."""
        return self._engine

    def test(self) -> bool:
        """Check database connectivity."""
        return self._engine.test_connection()

    @contextmanager
    def with_config(self, **overrides) -> Generator:
        """
        Scoped sync config override for this block.
        Example:
            with conn_manager.with_config(database="test_db"):
                db.execute("SELECT 1")
        """
        with override_thread_config(**overrides) as cfg:
            yield cfg

    @asynccontextmanager
    async def with_config_async(self, **overrides) -> AsyncGenerator:
        """
        Scoped async config override for this block.
        Example:
            async with conn_manager.with_config_async(database="test_db"):
                await db.execute("SELECT 1")
        """
        async with override_async_config(**overrides) as cfg:
            yield cfg

    @contextmanager
    def transaction(self):
        """Context-managed sync transaction."""
        try:
            self._engine.begin()
            yield self._engine
            self._engine.commit()
        except Exception:
            self._engine.rollback()
            raise

    @asynccontextmanager
    async def transaction_async(self):
        """Context-managed async transaction."""
        try:
            await self._engine.begin()
            yield self._engine
            await self._engine.commit()
        except Exception:
            await self._engine.rollback()
            raise

    def close(self):
        """Close underlying connection or pool."""
        self._engine.close()


# Global instance
connection_manager = ConnectionManager()
