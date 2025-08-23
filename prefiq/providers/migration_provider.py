# prefiq/providers/migration_provider.py

from __future__ import annotations
from prefiq.core.contracts.base_provider import BaseProvider
from prefiq.log.logger import get_logger
from prefiq.database.migrations.runner import migrate_all, drop_all
from prefiq.database.migrations.rollback import rollback

log = get_logger("prefiq.migrate")

class Migrator:
    def migrate(self, seed: bool = False) -> None:
        migrate_all()
        if seed:
            self.seed()

    def seed(self) -> None:
        log.info("seeding_start")
        # TODO: discover and run seeders here
        log.info("seeding_done")

    def fresh(self, seed: bool = False) -> None:
        drop_all()
        self.migrate(seed=seed)

    def rollback(self, steps: int = 1) -> None:
        rollback(step=steps)

class MigrationProvider(BaseProvider):
    def register(self) -> None:
        self.app.bind("migrator", Migrator())

    def boot(self) -> None:
        log.info("migrator_ready")
