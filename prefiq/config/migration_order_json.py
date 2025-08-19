import os
import json
from pathlib import Path
from prefiq.config.apps_cfg import get_registered_apps
from prefiq.settings.get_settings import load_settings


def _get_json_path(app: str) -> Path:
    """
    Get full path to `migration_order.json` for a given app.
    """
    project_root = Path(load_settings().project_root)
    return project_root / "apps" / app / "database" / "migration_order.json"


def ensure_migration_folder_and_json(app: str, overwrite: bool = False):
    """
    Ensure that database/migration folder and migration_order.json exist for a given app.
    Creates an empty JSON array if not present or if overwrite=True.
    """
    json_path = _get_json_path(app)
    json_path.parent.mkdir(parents=True, exist_ok=True)

    if not json_path.exists() or overwrite:
        with open(json_path, "w") as f:
            json.dump([], f)


def ensure_all_apps_have_migration_order():
    """
    Ensure migration folders and migration_order.json exist for all registered apps.
    """
    for app in get_registered_apps():
        ensure_migration_folder_and_json(app)


def delete_migration_json(app: str):
    """
    Delete the migration_order.json file for a given app.
    """
    json_path = _get_json_path(app)
    if json_path.exists():
        os.remove(json_path)


def read_migration_order(app: str) -> list[str]:
    """
    Return list of migrations from migration_order.json
    """
    json_path = _get_json_path(app)
    if not json_path.exists():
        return []
    with open(json_path) as f:
        return json.load(f)


def add_migration(app: str, filename: str):
    """
    Add a migration filename to the end of migration_order.json.
    Avoids duplicates.
    """
    order = read_migration_order(app)
    if filename not in order:
        order.append(filename)
        _write_json(app, order)


def remove_migration(app: str, filename: str):
    """
    Remove a migration filename from migration_order.json.
    """
    order = read_migration_order(app)
    if filename in order:
        order.remove(filename)
        _write_json(app, order)


def update_migration_at(app: str, index: int, filename: str):
    """
    Update a migration at a specific index.
    """
    order = read_migration_order(app)
    if 0 <= index < len(order):
        order[index] = filename
        _write_json(app, order)
    else:
        raise IndexError("Invalid index for migration update.")


def _write_json(app: str, data: list[str]):
    """
    Internal helper to write list to migration_order.json
    """
    json_path = _get_json_path(app)
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
