# prefiq/database/migrations/discover.py
from __future__ import annotations
import importlib.util
import importlib.machinery
import sys
from pathlib import Path
from typing import Iterable, List, Set, Tuple, Type

from prefiq.apps.app_cfg import get_registered_apps
from prefiq.settings.get_settings import load_settings
from prefiq.database.migrations.base import Migrations


def _candidate_dirs(project_root: str, app: str) -> Iterable[Path]:
    # 1) apps/<app>/database/migration
    yield Path(project_root) / "apps" / app / "database" / "migration"
    # 2) <app>/database/migration  (your current layout)
    yield Path(project_root) / "cortex" / "database" / "migrations"


def _migration_files(project_root: str, apps: Iterable[str]) -> Iterable[Path]:
    seen: Set[Path] = set()
    for app in apps:
        for p in _candidate_dirs(project_root, app):
            if not p.exists():
                continue
            for f in sorted(p.glob("*.py")):
                if f.name.startswith("_"):
                    continue
                if f not in seen:
                    seen.add(f)
                    yield f


def discover_all() -> List[Type[Migrations]]:
    """
    Discover migration classes across registered apps and return them ordered.
    Ensures modules are reloaded fresh each call so module-level state (e.g., CALLED)
    does not leak across tests.
    """
    settings = load_settings()
    project_root = getattr(settings, "project_root", str(Path.cwd()))
    apps = get_registered_apps()

    classes: List[Type[Migrations]] = []
    seen_keys: Set[Tuple[str, str]] = set()

    for file_path in _migration_files(project_root, apps):
        mod_name = file_path.stem  # keep simple name in sys.modules

        # Purge any stale module so the file is executed afresh
        if mod_name in sys.modules:
            del sys.modules[mod_name]

        spec = importlib.util.spec_from_file_location(mod_name, str(file_path))
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        loader = spec.loader  # type: ignore[assignment]
        assert isinstance(loader, importlib.machinery.SourceFileLoader)
        loader.exec_module(module)
        sys.modules[mod_name] = module

        for attr in module.__dict__.values():
            if isinstance(attr, type) and issubclass(attr, Migrations) and attr is not Migrations:
                app = getattr(attr, "APP_NAME", "core")
                name = getattr(attr, "TABLE_NAME", attr.__name__)
                key = (app, name)
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                classes.append(attr)

    def _order_key(cls: Type[Migrations]):
        idx = int(getattr(cls, "ORDER_INDEX", 0))
        app = getattr(cls, "APP_NAME", "core")
        name = getattr(cls, "TABLE_NAME", cls.__name__)
        return (idx, app, name)

    classes.sort(key=_order_key)
    return classes
