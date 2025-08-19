# apps/devmeta/provider.py
from typing import Optional

from apps.devmeta.cli.devmeta import mount_devmeta_cli
from apps.devmeta.core.helper import resolve_sqlite_path, DEFAULT_SQLITE_PATH, ensure_dir_for
from apps.devmeta.core.migrator import DevMetaMigrator
from apps.devmeta.services.todo import bind_todo_service
from prefiq.core.contracts.base_provider import BaseProvider
from prefiq.log.logger import get_logger

LOG = get_logger("prefiq.devmeta.provider")

class DevMetaProvider(BaseProvider):
    """
    Prefiq-style provider for DevMeta (SQLite local DB + Python migrations).
    """
    def __init__(self, app) -> None:
        super().__init__(app)
        self.sqlite_path: Optional[str] = None

    def register(self) -> None:
        LOG.info("register_start")

        # Resolve settings (duck-typed)
        try:
            settings = self.app.resolve("settings")
        except Exception:
            settings = None

        # Pick SQLite path and ensure its directory exists
        path = resolve_sqlite_path(settings) or DEFAULT_SQLITE_PATH
        ensure_dir_for(path)
        self.sqlite_path = path
        LOG.info("sqlite_path_resolved", extra={"path": self.sqlite_path})

        # Bind path for others to discover
        try:
            self.app.bind("devmeta.sqlite_path", self.sqlite_path)
        except Exception:
            pass

        # Bind migrator (+ generic alias)
        migrator = DevMetaMigrator(db_path=self.sqlite_path)
        try:
            self.app.bind("devmeta.migrator", migrator)
            self.app.bind("migrator", migrator)  # <-- important alias
            LOG.info("migrator_bound")
        except Exception as e:
            LOG.error("migrator_bind_failed", extra={"error": repr(e)})

        # Optional services
        try:
            bind_todo_service(self.app, db_path=self.sqlite_path)
        except Exception as e:
            LOG.error("todo_service_bind_failed", extra={"error": repr(e)})

        LOG.info("register_done")

    def boot(self) -> None:
        LOG.info("boot_start")
        try:
            mount_devmeta_cli(self.app)
        except Exception as e:
            LOG.error("cli_mount_failed", extra={"error": repr(e)})
        LOG.info("boot_done")
