# prefiq/providers/database_provider.py
from __future__ import annotations

import asyncio
import atexit
import inspect
import os
import sys
from typing import Any, Optional

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
            if getattr(s, "DB_CLOSE_ATEXIT", True) and str(getattr(s, "DB_MODE", "sync")).lower() != "async":
                atexit.register(self._shutdown_sync_only)
        except Exception:
            pass

    def boot(self) -> None:
        """
        Best-effort warmup — but ONLY for the active engine (or explicit test flags).
        Previously this always tried MariaDB prewarm if DB_POOL_WARMUP>0, which caused
        MariaDB connection attempts even on SQLite.
        """
        s = self._get_settings_safe()

        # Resolve warmup count from settings or env
        warm = 0
        try:
            if s and hasattr(s, "DB_POOL_WARMUP"):
                warm = int(getattr(s, "DB_POOL_WARMUP") or 0)
            else:
                warm = int(os.getenv("DB_POOL_WARMUP", "0") or "0")
        except (ValueError, TypeError):
            warm = 0

        if warm <= 0:
            return

        engine_name = (str(getattr(s, "DB_ENGINE", "")).lower() if s else os.getenv("DB_ENGINE", "")).lower()
        test_pg = bool(getattr(s, "DB_TEST_PG", False)) if s else (os.getenv("DB_TEST_PG", "0") not in ("0", "", "false", "False"))
        test_mysql = bool(getattr(s, "DB_TEST_MYSQL", False)) if s else (os.getenv("DB_TEST_MYSQL", "0") not in ("0", "", "false", "False"))

        coro: Optional[object] = None

        try:
            # MariaDB / MySQL warmup
            if engine_name in ("mariadb", "mysql") or test_mysql:
                from prefiq.database.engines.mariadb.pool import prewarm as _mariadb_prewarm  # lazy import
                coro = _mariadb_prewarm(warm)

            # Postgres warmup
            elif engine_name in ("postgres", "postgresql") or test_pg:
                from prefiq.database.engines.postgres.pool import prewarm as _pg_prewarm  # lazy import
                coro = _pg_prewarm(warm)

            # SQLite or anything else: no warmup needed / supported
            else:
                coro = None

        except (ModuleNotFoundError, ImportError, AttributeError, ValueError, TypeError):
            coro = None

        # Run warmup if applicable
        if coro and inspect.isawaitable(coro):
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                asyncio.run(coro)
            else:
                asyncio.create_task(coro)

    def _get_settings_safe(self):
        try:
            # Prefer container-bound settings (if any)
            s = self.app.resolve("settings")
            if s:
                return s
        except Exception:
            pass
        try:
            return load_settings()
        except Exception:
            return None

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
            if hasattr(eng, "close"):
                res = eng.close()
                if inspect.isawaitable(res):
                    return
        except Exception:
            pass
