from __future__ import annotations
from prefiq.core.contracts.base_provider import BaseProvider
from prefiq.utils.logger import get_logger

# import your migration modules
from cortex.database.base_tables.m000_migration_table import up as migrations_table_up  # ensure exists
from prefiq.database.migrations.runner import migrate_all, drop_all
from prefiq.database.migrations.rollback import rollback

log = get_logger("prefiq.migrate")

class Migrator:
    def migrate(self, seed: bool = False) -> None:
        migrations_table_up()
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
        try:
            migrations_table_up()
            log.info("migrations_table_ready")
        except Exception as e:
            log.error("migrations_table_error", extra={"error": str(e)})
            raise
