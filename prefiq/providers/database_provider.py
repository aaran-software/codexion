import atexit

from prefiq.core.contracts.base_provider import BaseProvider
from prefiq.database.connection import get_engine
from prefiq.settings.get_settings import get_settings
from prefiq.providers.schemas.database import DatabaseSettings
from prefiq.utils.logger import get_logger
import asyncio, inspect
from contextlib import suppress

class DatabaseProvider(BaseProvider):
    def __init__(self, app):
        super().__init__(app)
        self.engine = None
        s = get_settings()
        self.log = get_logger(f"{s.LOG_NAMESPACE}.db.provider")
        self._teardown_registered = False

    def register(self) -> None:
        self.engine = get_engine()
        self.app.bind("db", self.engine)
        self.log.debug("db_registered", extra={"engine_type": type(self.engine).__name__})

        # register one-time process-exit teardown
        if not self._teardown_registered:
            atexit.register(self._close_engine_safely)
            self._teardown_registered = True

    def _close_engine_safely(self):
        try:
            if hasattr(self.engine, "close"):
                res = self.engine.close()
                # handle async close too
                res = self._resolve_awaitable(res)
            self.log.info("db_closed")
        except Exception as e:
            self.log.error("db_close_error", extra={"error": str(e)})

    @staticmethod
    def _resolve_awaitable(maybe_awaitable):
        if inspect.iscoroutine(maybe_awaitable):
            return asyncio.run(maybe_awaitable)
        if inspect.isawaitable(maybe_awaitable):
            loop = asyncio.get_event_loop_policy().new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                task = asyncio.ensure_future(maybe_awaitable)
                return loop.run_until_complete(task)
            finally:
                with suppress(Exception):
                    loop.run_until_complete(loop.shutdown_asyncgens())
                asyncio.set_event_loop(None)
                loop.close()
        return maybe_awaitable

    def boot(self) -> None:
        s = get_settings()
        try:
            DatabaseSettings.model_validate(
                dict(DB_ENGINE=s.DB_ENGINE, DB_MODE=s.DB_MODE, DB_HOST=s.DB_HOST,
                     DB_PORT=s.DB_PORT, DB_USER=s.DB_USER, DB_PASS=s.DB_PASS, DB_NAME=s.DB_NAME)
            )
        except Exception as e:
            self.log.error("db_settings_invalid", extra={"error": str(e)})
            raise

        self.log.info("db_settings", extra={
            "engine": s.DB_ENGINE, "mode": s.DB_MODE, "host": s.DB_HOST,
            "port": s.DB_PORT, "db": s.DB_NAME, "user": s.DB_USER
        })

        try:
            ok = self._resolve_awaitable(self.engine.test_connection())
            if not ok:
                try:
                    probe = self._resolve_awaitable(self.engine.fetchone("SELECT 1"))
                    ok = probe is not None
                except Exception as probe_err:
                    self.log.error("db_probe_error", extra={"error": str(probe_err)})
                    raise

            level = self.log.info if ok else self.log.error
            level("db_connectivity", extra={"ok": bool(ok)})
        except (ConnectionError, OSError, TimeoutError, asyncio.TimeoutError) as e:
            self.log.error("db_connectivity_error", extra={"error": str(e)})
            raise
        except RuntimeError as e:
            self.log.error("db_runtime_error", extra={"error": str(e)})
            raise
