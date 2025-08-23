# prefiq/providers/database_provider.py

# prefiq/providers/database_provider.py
from __future__ import annotations

import atexit
import os
from typing import Any

from prefiq.core.contracts.base_provider import BaseProvider  # adjust if your path differs
from prefiq.database.connection import get_engine, reset_engine
from prefiq.database.connection_manager import connection_manager
from prefiq.database.engines.abstract_engine import AbstractEngine
from prefiq.database.engines.mariadb.pool import prewarm, close_pool
# from prefiq.database.hooks import default_before_hook, default_after_hook

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
        engine.set_before_execute_hook(default_before_hook)
        engine.set_after_execute_hook(default_after_hook)
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
        try:
            # MariaDB async pool
            self.app.run_async(close_pool())  # best-effort if async
        except Exception:
            pass
        try:
            # Engines often expose close(); our connection layer has reset_engine()
            connection_manager.close()
        except Exception:
            pass
        try:
            reset_engine()
        except Exception:
            pass
