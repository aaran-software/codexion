# prefiq/providers/migration_provider.py
from __future__ import annotations

from prefiq.core.application import BaseProvider, register_provider
from prefiq.database.migrations.runner import migrate_all, drop_all
from prefiq.database.migrations.rollback import rollback
from prefiq.database.schemas.builder import ensure_migrations_table


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
        rollback(step=steps)


@register_provider
class MigrationProvider(BaseProvider):
    def register(self) -> None:
        self.app.bind("migrator", Migrator())

    def boot(self) -> None:
        # Ensure the meta 'migrations' table exists at boot time
        ensure_migrations_table()
