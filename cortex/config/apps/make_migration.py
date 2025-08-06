import os
import json
from pathlib import Path
from cortex.config.apps.migration_order_json import (
    ensure_migration_folder_and_json,
    read_migration_order,
    add_migration,
    remove_migration,
    update_migration_at
)
from cortex.core.settings import get_settings


MIGRATION_TEMPLATE = """from cortex.database.schemas.builder import create, dropIfExists

def up():
    create("{table_name}", lambda table: [
        table.id(),
        table.string("name"),
        table.timestamps()
    ])

def down():
    dropIfExists("{table_name}")
"""

def _get_migration_path(app: str) -> Path:
    project_root = Path(get_settings().project_root)
    return project_root / "apps" / app / "database" / "migration"

def create_migration_file(app: str, table_name: str) -> str:
    ensure_migration_folder_and_json(app)

    migration_dir = _get_migration_path(app)
    migration_order = read_migration_order(app)
    next_index = len(migration_order) + 1
    filename = f"{next_index:03d}_{table_name}.py"
    filepath = migration_dir / filename

    if filepath.exists():
        raise FileExistsError(f"Migration file '{filename}' already exists.")

    # Write migration template
    with open(filepath, "w") as f:
        f.write(MIGRATION_TEMPLATE.format(table_name=table_name))

    # Register migration
    add_migration(app, filename)
    print(f"✅ Created migration: {filename}")
    return filename

def delete_migration_file(app: str, filename: str):
    migration_dir = _get_migration_path(app)
    filepath = migration_dir / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Migration file '{filename}' not found.")

    os.remove(filepath)
    remove_migration(app, filename)
    print(f"🗑️ Deleted migration: {filename}")

def update_migration_filename(app: str, old_filename: str, new_table_name: str):
    migration_dir = _get_migration_path(app)
    migration_order = read_migration_order(app)

    if old_filename not in migration_order:
        raise ValueError(f"Migration '{old_filename}' not found in order list.")

    index = migration_order.index(old_filename)
    new_filename = f"{index+1:03d}_{new_table_name}.py"

    old_path = migration_dir / old_filename
    new_path = migration_dir / new_filename

    if not old_path.exists():
        raise FileNotFoundError(f"Old migration file '{old_filename}' not found.")

    os.rename(old_path, new_path)
    update_migration_at(app, index, new_filename)
    print(f"✏️ Renamed migration: {old_filename} → {new_filename}")
    return new_filename
