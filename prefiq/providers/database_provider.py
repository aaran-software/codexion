# prefiq/providers/database_provider.py

from __future__ import annotations

import atexit
import asyncio
import inspect
import logging
from contextlib import suppress

from prefiq.core.contracts.base_provider import BaseProvider
from prefiq.database.connection import get_engine
from prefiq.settings.get_settings import load_settings
from prefiq.log.logger import get_logger

from prefiq.providers.db_config import DatabaseSettings


class DatabaseProvider(BaseProvider):
    # lets SettingsProvider validate this provider early (optional but nice)
    schema_model = DatabaseSettings

    def __init__(self, app):
        super().__init__(app)
        self.engine = None
        s = load_settings()
        self.log = get_logger(f"{s.LOG_NAMESPACE}.db.provider")
        self._teardown_registered = False

    def register(self) -> None:
        # Build engine from current settings
        self.engine = get_engine()
        self.app.bind("db", self.engine)
        self.log.debug("db_registered", extra={"engine_type": type(self.engine).__name__})

        # Honor settings flag before registering atexit
        s = load_settings()
        if getattr(s, "DB_CLOSE_ATEXIT", True) and not self._teardown_registered:
            atexit.register(self._close_engine_safely)
            self._teardown_registered = True

    def _close_engine_safely(self) -> None:
        try:
            if hasattr(self.engine, "close"):
                res = self.engine.close()
                self._resolve_awaitable(res)

            # avoid logging if handlers are torn down during interpreter shutdown
            try:
                root = logging.getLogger()
                if any(
                    hasattr(h, "stream") and getattr(h.stream, "closed", False) is False
                    for h in root.handlers
                ):
                    self.log.info("db_closed")
            except Exception:
                pass
        except Exception as e:
            try:
                self.log.error("db_close_error", extra={"error": str(e)})
            except Exception:
                pass

    @staticmethod
    def _resolve_awaitable(maybe_awaitable):
        """Await if needed. Works even if an event loop is already running."""
        if inspect.isawaitable(maybe_awaitable) or inspect.iscoroutine(maybe_awaitable):
            try:
                # If there's no running loop, asyncio.run is fine
                asyncio.get_running_loop()
            except RuntimeError:
                return asyncio.run(maybe_awaitable)
            else:
                # Running loop present → use a private loop to await
                new_loop = asyncio.new_event_loop()
                try:
                    asyncio.set_event_loop(new_loop)
                    task = new_loop.create_task(maybe_awaitable)  # <-- create task on this loop
                    return new_loop.run_until_complete(task)
                finally:
                    with suppress(Exception):
                        new_loop.run_until_complete(new_loop.shutdown_asyncgens())
                    asyncio.set_event_loop(None)
                    new_loop.close()
        return maybe_awaitable

    def boot(self) -> None:
        s = load_settings()

        # Validate DB env with schema (supports mariadb or sqlite)
        try:
            DatabaseSettings.model_validate(
                dict(
                    DB_ENGINE=s.DB_ENGINE,
                    DB_MODE=s.DB_MODE,
                    DB_HOST=getattr(s, "DB_HOST", None),
                    DB_PORT=getattr(s, "DB_PORT", None),
                    DB_USER=getattr(s, "DB_USER", None),
                    DB_PASS=getattr(s, "DB_PASS", None),
                    DB_NAME=s.DB_NAME,
                    DB_POOL_WARMUP=getattr(s, "DB_POOL_WARMUP", 1),
                )
            )
        except Exception as e:
            self.log.error("db_settings_invalid", extra={"error": str(e)})
            raise

        self.log.info(
            "db_settings",
            extra={
                "engine": s.DB_ENGINE,
                "mode": s.DB_MODE,
                "host": getattr(s, "DB_HOST", None),
                "port": getattr(s, "DB_PORT", None),
                "db": s.DB_NAME,
                "user": getattr(s, "DB_USER", None),
            },
        )

        # Connectivity probe (works for sync or async engines)
        try:
            ok = self._resolve_awaitable(getattr(self.engine, "test_connection")())
            if not ok:
                try:
                    probe = self._resolve_awaitable(self.engine.fetchone("SELECT 1"))
                    ok = probe is not None
                except Exception as probe_err:
                    self.log.error("db_probe_error", extra={"error": str(probe_err)})
                    raise

            (self.log.info if ok else self.log.error)("db_connectivity", extra={"ok": bool(ok)})
        except (ConnectionError, OSError, TimeoutError, asyncio.TimeoutError) as e:
            self.log.error("db_connectivity_error", extra={"error": str(e)})
            raise
        except RuntimeError as e:
            self.log.error("db_runtime_error", extra={"error": str(e)})
            raise
