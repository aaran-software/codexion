# cortex/database/migrations/migration_provider.py

import os
from typing import Dict
from cortex.database.migrations.runner import BaseMigrationRunner
from cortex.database.migrations.file import list_migration_files


class MigrationServiceProvider:
    def __init__(self, runner: BaseMigrationRunner):
        self.runner = runner
        self.folder_map: Dict[str, str] = {}

    def map_migrations(self, module_name: str, folder_path: str) -> None:
        """
        Register a new migration folder for a given module.
        """
        if not os.path.isdir(folder_path):
            raise ValueError(f"Migration folder does not exist: {folder_path}")
        self.folder_map[module_name] = folder_path

    def register_all(self):
        """
        Register migrations from all mapped folders into the runner.
        """
        for module, path in self.folder_map.items():
            files = list_migration_files(path)
            print(f"📦 Registering {len(files)} migrations from: {module}")
            for file in files:
                self.runner.register_from_module(file)
