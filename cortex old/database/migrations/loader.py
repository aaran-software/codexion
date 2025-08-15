# cortex/database/migrations/loader.py

import os
import configparser
import json
import importlib.util
from types import ModuleType
from typing import Tuple, List, Dict

from cortex.config.apps.apps_cfg import get_registered_apps
from cortex.core.settings import get_settings
from cortex.database.migrations.hashing import compute_file_hash

settings = get_settings()
PROJECT_ROOT = settings.project_root
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "apps.cfg")


def resolve_migration_path(app: str, migration_name: str) -> str:
    """
    Resolve full path of a specific migration file from an app.
    """
    path = os.path.join(PROJECT_ROOT, "apps", app, "database", "migration", f"{migration_name}.py")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Migration file not found: {path}")
    return path


def load_migration_order(app: str) -> List[str]:
    """
    Load ordered list of migration files from apps/<app>/database/migration_order.json
    """
    path = os.path.join(PROJECT_ROOT, "apps", app, "database", "migration_order.json")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing migration_order.json for app: {app}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_migration_module(file_path: str) -> ModuleType:
    """
    Dynamically import a migration file and return its module object.
    """
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import migration module at {file_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def resolve_and_load(app: str, migration_name: str) -> Tuple[ModuleType, str]:
    """
    Resolve file path, compute hash, load module.
    Returns: (module, hash)
    """
    path = resolve_migration_path(app, migration_name)
    hash = compute_file_hash(path)
    mod = load_migration_module(path)
    return mod, hash


def discover_all_app_migrations() -> Dict[str, List[str]]:
    """
    From all registered apps (via apps.cfg), load their migration order.
    Returns: { "app_name": [migration1, migration2, ...] }
    """
    result = {}
    for app in get_registered_apps():
        try:
            order = load_migration_order(app)
            result[app] = order
        except FileNotFoundError:
            # Skip if no migration_order.json
            continue
    return result
