# =============================================================
# Migration Runner System (OOP-based)
#
# Author: ChatGPT
# Created: 2025-08-06
#
# Purpose:
#   - system to register and apply migrations.
#   - Allows folder-based scanning or manual registration via ServiceProvider.
# =============================================================

import os
import importlib.util
from typing import List, Callable
from cortex.database.engines.mariadb.sync_engine import SyncMariaDBEngine
from cortex.database.migrations.tracker import MigrationTracker


class Migration:
    def __init__(self, name: str, up: Callable, down: Callable):
        self.name = name
        self.up = up
        self.down = down


class BaseMigrationRunner:
    def __init__(self, engine: SyncMariaDBEngine):
        self.engine = engine
        self.tracker = MigrationTracker(engine)
        self.migrations: List[Migration] = []

    def register(self, migration: Migration):
        self.migrations.append(migration)

    def register_from_module(self, path: str):
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.register(Migration(name, getattr(module, "up"), getattr(module, "down")))

    def scan_folder(self, folder: str):
        for file in sorted(os.listdir(folder)):
            if file.endswith(".py") and not file.startswith("__"):
                self.register_from_module(os.path.join(folder, file))

    def migrate(self):
        self.engine.connect()
        self.tracker.ensure_table()
        applied = self.tracker.get_applied_migrations()
        batch = self.tracker.get_latest_batch() + 1

        for migration in self.migrations:
            if migration.name not in applied:
                print(f" Migrating: {migration.name}")
                migration.up()
                self.tracker.record_migration(migration.name, batch)



