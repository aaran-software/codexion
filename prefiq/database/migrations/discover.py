# prefiq/database/migrations/discover.py
from __future__ import annotations
import os, sys, glob, importlib.util
from types import ModuleType
from typing import List, Type

from prefiq.settings.get_settings import load_settings
from prefiq.apps.apps_cfg import get_registered_apps
from prefiq.database.migrations.base import Migrations

def _import_py(path: str) -> ModuleType:
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import migration module at {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # keep a weak mapping so sys.modules has a stable ref for hashing later
    sys.modules.setdefault(name, mod)
    return mod

def import_all_migration_modules() -> List[ModuleType]:
    """Import all *.py under apps/<app>/database/migration and optional cortex/database/migration."""
    s = load_settings()
    root = s.project_root
    loaded: List[ModuleType] = []

    # App-scoped migrations: apps/<app>/database/migration/*.py
    for app in get_registered_apps():
        folder = os.path.join(root, "apps", app, "database", "migration")
        if not os.path.isdir(folder):
            continue
        for path in sorted(glob.glob(os.path.join(folder, "*.py"))):
            base = os.path.basename(path)
            if base.startswith("_"):
                continue
            loaded.append(_import_py(path))

    # Optional: core/cortex migrations too, if you keep any there
    extra = os.path.join(root, "cortex", "database", "migration")
    if os.path.isdir(extra):
        for path in sorted(glob.glob(os.path.join(extra, "*.py"))):
            base = os.path.basename(path)
            if base.startswith("_"):
                continue
            loaded.append(_import_py(path))

    return loaded

def discover_all() -> List[Type[Migrations]]:
    """Load all modules, then return subclasses of Migrations ordered by ORDER_INDEX."""
    import_all_migration_modules()
    return sorted(Migrations.__subclasses__(), key=lambda c: c.ORDER_INDEX)
