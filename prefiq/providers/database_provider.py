# prefiq/providers/database_provider.py
from __future__ import annotations

import asyncio
import atexit
import inspect
import os
import sys
from typing import Any

from prefiq.core.application import BaseProvider, register_provider
from prefiq.settings.get_settings import load_settings
from prefiq.database.connection import get_engine
from prefiq.database.engines.abstract_engine import AbstractEngine
from prefiq.database.hooks import before_execute, after_execute


@register_provider
class DatabaseProvider(BaseProvider):
    """
    Binds 'db' (engine singleton) into the container and attaches hooks.
    Centralized shutdown is handled by FastAPI's shutdown event.
    atexit is only registered for SYNC engines (no async work during interpreter finalization).
    """

    def register(self) -> None:
        engine: AbstractEngine[Any] = get_engine()

        # Attach optional hooks if engine supports them
        try:
            if hasattr(engine, "set_before_execute_hook") and callable(getattr(engine, "set_before_execute_hook")):
                engine.set_before_execute_hook(before_execute)
            if hasattr(engine, "set_after_execute_hook") and callable(getattr(engine, "set_after_execute_hook")):
                engine.set_after_execute_hook(after_execute)
        except (ValueError, TypeError):
            pass

        self.app.bind("db", engine)

        # Register atexit fallback ONLY for sync engines
        try:
            s = load_settings()
            if getattr(s, "DB_CLOSE_ATEXIT", True) and getattr(s, "DB_MODE", "sync").lower() != "async":
                atexit.register(self._shutdown_sync_only)
        except Exception:
            pass

    def boot(self) -> None:
        # Best-effort warmup (MariaDB async pool)
        warm = 0
        try:
            s = self.app.resolve("settings")
            if s and hasattr(s, "DB_POOL_WARMUP"):
                warm = int(getattr(s, "DB_POOL_WARMUP") or 0)
            else:
                warm = int(os.getenv("DB_POOL_WARMUP", "0") or "0")
        except (ValueError, TypeError):
            warm = 0

        if warm > 0:
            try:
                # Import lazily to avoid importing MariaDB bits for other engines
                from prefiq.database.engines.mariadb.pool import prewarm as _mariadb_prewarm  # type: ignore
                coro = _mariadb_prewarm(warm)
                if inspect.isawaitable(coro):
                    try:
                        asyncio.get_running_loop()
                    except RuntimeError:
                        asyncio.run(coro)
                    else:
                        asyncio.create_task(coro)
            except (ModuleNotFoundError, ImportError, AttributeError, ValueError, TypeError):
                pass

    @staticmethod
    def _shutdown_sync_only() -> None:
        """
        Best-effort close for *sync* engines only.
        Never schedule async work here — process is exiting.
        """
        if getattr(sys, "is_finalizing", lambda: False)():
            return
        try:
            eng = get_engine()
            # Call close if it's sync; if it's awaitable, skip (FastAPI shutdown handled it)
            if hasattr(eng, "close"):
                res = eng.close()
                if inspect.isawaitable(res):
                    return
        except Exception:
            pass
