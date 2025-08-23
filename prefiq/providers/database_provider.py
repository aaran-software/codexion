# prefiq/providers/database_provider.py
from __future__ import annotations

import asyncio
import atexit
import inspect
import os
from typing import Any

from prefiq.core.contracts.base_provider import BaseProvider
from prefiq.database.connection import get_engine, reset_engine
from prefiq.database.connection_manager import connection_manager
from prefiq.database.engines.abstract_engine import AbstractEngine
from prefiq.database.hooks import before_execute, after_execute

# MariaDB async pool helpers are optional; import inside guards when used.


class DatabaseProvider(BaseProvider):
    """
    Binds 'db' (engine singleton) into the container.

    - Hooks (before/after) are OPTIONAL: set them only if the engine supports it.
    - MariaDB async pool prewarm is best-effort (no-op for other engines).
    - Registers a clean shutdown to close pools/handles on process exit.
    """

    def register(self) -> None:
        # Construct (or reuse) the engine and bind into app container
        engine: AbstractEngine[Any] = get_engine()

        # Set default hooks only if the engine exposes the API (PG engines may not)
        try:
            if hasattr(engine, "set_before_execute_hook") and callable(getattr(engine, "set_before_execute_hook")):
                engine.set_before_execute_hook(before_execute)
            if hasattr(engine, "set_after_execute_hook") and callable(getattr(engine, "set_after_execute_hook")):
                engine.set_after_execute_hook(after_execute)
        except Exception:
            # Hooks are convenience features; never block provider registration on them
            pass

        self.app.bind("db", engine)

    def boot(self) -> None:
        # Optional: prewarm MariaDB async pool (harmless no-op elsewhere)
        warm = 0
        try:
            warm = int(os.getenv("DB_POOL_WARMUP", "0") or "0")
        except Exception:
            warm = 0

        if warm > 0:
            try:
                # Import lazily to avoid importing MariaDB bits for other engines
                from prefiq.database.engines.mariadb.pool import prewarm as _mariadb_prewarm  # type: ignore

                coro = _mariadb_prewarm(warm)
                # Run the coroutine whether or not an event loop is present
                if inspect.isawaitable(coro):
                    try:
                        asyncio.get_running_loop()
                    except RuntimeError:
                        asyncio.run(coro)
                    else:
                        asyncio.create_task(coro)
            except Exception:
                # Best-effort only; don't fail boot if prewarm is unavailable
                pass

        # Ensure pools/engines are cleaned up on interpreter exit
        atexit.register(self._shutdown)

    def _shutdown(self) -> None:
        """Close pools (async) and engine (sync/async) safely at process exit."""
        # MariaDB async pool close (if present)
        try:
            from prefiq.database.engines.mariadb.pool import close_pool as _close_pool  # type: ignore

            res = _close_pool()
            if inspect.isawaitable(res):
                try:
                    asyncio.get_running_loop()
                except RuntimeError:
                    asyncio.run(res)
                else:
                    asyncio.create_task(res)
        except Exception:
            pass

        # Close connection manager (handles per-engine specifics)
        try:
            connection_manager.close()
        except Exception:
            pass

        # Reset engine singleton
        try:
            reset_engine()
        except Exception:
            pass
