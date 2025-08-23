# prefiq/providers/database_provider.py

# prefiq/providers/database_provider.py
from __future__ import annotations

import asyncio
import atexit
import inspect
import os
from typing import Any

from prefiq.core.contracts.base_provider import BaseProvider  # adjust if your path differs
from prefiq.database.connection import get_engine, reset_engine
from prefiq.database.connection_manager import connection_manager
from prefiq.database.engines.abstract_engine import AbstractEngine
from prefiq.database.engines.mariadb.pool import prewarm, close_pool
from prefiq.database.hooks import before_execute, after_execute

class DatabaseProvider(BaseProvider):
    """
    Binds 'db' (engine singleton) into the container.
    - Sets default before/after hooks (can be replaced later).
    - Optionally pre-warms MariaDB pool based on env.
    - Closes pools/handles at process exit.
    """

    def register(self) -> None:
        # Construct (or reuse) the engine and bind into app container
        engine: AbstractEngine[Any] = get_engine()
        # Set default hooks (users can override later)
        engine.set_before_execute_hook(before_execute)
        engine.set_after_execute_hook(after_execute)
        self.app.bind("db", engine)

    def boot(self) -> None:
        # Optional: prewarm MariaDB pool if env says so
        warm = int(os.getenv("DB_POOL_WARMUP", "0") or "0")
        if warm > 0:
            try:
                # Only MariaDB async pool exposes prewarm; noop for others
                self.app.logger.info(f"DB: prewarming {warm} MariaDB connections")
                self.app.run_async(prewarm(warm))  # if your app has a helper to run coroutines
            except Exception:
                # best effort; don't block boot
                pass

        # Close pool/engine at process exit
        atexit.register(self._shutdown)

    def _shutdown(self) -> None:
        # Close pool (async) and engine (sync/async) safely.
        try:
            from prefiq.database.engines.mariadb.pool import close_pool
            res = close_pool()
            if inspect.isawaitable(res):
                try:
                    asyncio.get_running_loop()
                except RuntimeError:
                    asyncio.run(res)
                else:
                    asyncio.create_task(res)
        except Exception:
            pass

        # Engine close via connection_manager / reset_engine (already await-aware)
        try:
            from prefiq.database.connection_manager import connection_manager
            connection_manager.close()
        except Exception:
            pass
        try:
            from prefiq.database.connection import reset_engine
            reset_engine()
        except Exception:
            pass
