# prefiq/providers/migration_provider.py
from __future__ import annotations

import os

from mariadb import OperationalError

from prefiq.core.application import BaseProvider, register_provider
from prefiq.database.migrations.runner import migrate_all, drop_all
from prefiq.database.migrations.rollback import rollback
from prefiq.database.schemas.builder import ensure_migrations_table
from prefiq.core.logger import log


class Migrator:
    def migrate(self, seed: bool = False) -> None:
        ensure_migrations_table()
        migrate_all()
        if seed:
            self.seed()

    def seed(self) -> None:
        # TODO: discover and run seeders here
        pass

    def fresh(self, seed: bool = False) -> None:
        drop_all(include_protected=True)
        ensure_migrations_table()
        self.migrate(seed=seed)

    def rollback(self, steps: int = 1) -> None:
        rollback(steps)


@register_provider
class MigrationProvider(BaseProvider):
    def register(self) -> None:
        self.app.bind("migrator", Migrator())

    def boot(self) -> None:
        if os.getenv("PREFIQ_SKIP_MIGRATIONS", "0") in ("1", "true", "yes"):
            return
        try:
            ensure_migrations_table()
        except OperationalError as e:
            msg = (
                "Database connection failed while ensuring the 'migrations' table. "
                "Check DB_* environment variables or switch to SQLite for local runs."
            )
            # pick one of these depending on your style:
            # raise RuntimeError(msg) from e
            log.error("%s (%s)", msg, e)
            raise
