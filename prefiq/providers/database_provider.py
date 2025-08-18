import atexit
import asyncio, inspect
import logging
from contextlib import suppress

from prefiq.core.contracts.base_provider import BaseProvider
from prefiq.database.connection import get_engine
from prefiq.settings.get_settings import load_settings
from prefiq.log.logger import get_logger

# NEW: import your DB settings schema (create this if you don't have it yet)
# File suggestion: prefiq/providers/db_config.py (see below)
from prefiq.providers.db_config import DatabaseSettings  # NEW


class DatabaseProvider(BaseProvider):
    def __init__(self, app):
        super().__init__(app)
        self.engine = None
        s = load_settings()
        self.log = get_logger(f"{s.LOG_NAMESPACE}.db.provider")
        self._teardown_registered = False

    def register(self) -> None:
        self.engine = get_engine()
        self.app.bind("db", self.engine)
        self.log.debug("db_registered", extra={"engine_type": type(self.engine).__name__})

        # honor settings flag before registering atexit
        s = load_settings()
        if getattr(s, "DB_CLOSE_ATEXIT", True) and not self._teardown_registered:
            atexit.register(self._close_engine_safely)
            self._teardown_registered = True

    def _close_engine_safely(self):
        try:
            if hasattr(self.engine, "close"):
                res = self.engine.close()
                res = self._resolve_awaitable(res)
            # avoid logging if logging handlers are gone during interpreter shutdown
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
        # NEW: handle "already running loop" cases safely
        if inspect.isawaitable(maybe_awaitable) or inspect.iscoroutine(maybe_awaitable):
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                # no running loop → we can use asyncio.run directly
                return asyncio.run(maybe_awaitable)
            else:
                # running loop → create a private loop to await
                new_loop = asyncio.new_event_loop()
                try:
                    return new_loop.run_until_complete(asyncio.ensure_future(maybe_awaitable, loop=new_loop))
                finally:
                    with suppress(Exception):
                        new_loop.run_until_complete(new_loop.shutdown_asyncgens())
                    new_loop.close()
        return maybe_awaitable

    def boot(self) -> None:
        s = load_settings()
        # NEW: validate DB env with a schema (optional but recommended)
        try:
            DatabaseSettings.model_validate(
                dict(
                    DB_ENGINE=s.DB_ENGINE,
                    DB_MODE=s.DB_MODE,
                    DB_HOST=s.DB_HOST,
                    DB_PORT=s.DB_PORT,
                    DB_USER=s.DB_USER,
                    DB_PASS=s.DB_PASS,
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
                "host": s.DB_HOST,
                "port": s.DB_PORT,
                "db": s.DB_NAME,
                "user": s.DB_USER,
            },
        )

        # connectivity probe
        try:
            ok = self._resolve_awaitable(self.engine.test_connection())
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
