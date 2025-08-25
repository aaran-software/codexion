# prefiq/database/migrations/discover.py
from __future__ import annotations
import importlib.util
import importlib.machinery
import sys, hashlib
from pathlib import Path
from typing import Iterable, List, Set, Tuple, Type

from prefiq.apps.app_cfg import get_registered_apps
from prefiq.settings.get_settings import load_settings
from prefiq.database.migrations.base import Migrations


def _candidate_dirs(project_root: Path, app: str) -> Iterable[Path]:
    # 1) apps/<app>/database/migrations   ← FIX: plural
    yield project_root / "apps" / app / "database" / "migrations"
    # 2) <app>/database/migrations        ← FIX: generic top-level (works for 'cortex' *if* it’s registered)
    yield project_root / app / "database" / "migrations"


def _migration_files(project_root: Path, apps: Iterable[str]) -> Iterable[tuple[str, Path]]:
    seen: Set[Path] = set()
    for app in apps:
        for p in _candidate_dirs(project_root, app):
            if not p.exists():
                continue
            for f in sorted(p.glob("*.py")):
                if f.name.startswith("_"):
                    continue
                if f in seen:
                    continue
                seen.add(f)
                yield app, f


def _unique_mod_name(app: str, file_path: Path) -> str:
    # Avoid collisions when different apps use the same filename (e.g., 0001_init.py)
    h = hashlib.sha1(str(file_path).encode("utf-8")).hexdigest()[:8]
    return f"prefiq.migrations.{app}.{file_path.stem}_{h}"


def _derived_table_name(cls: Type[Migrations]) -> str:
    # Keep consistent with runner: prefer derived_table_name() if available
    return cls.derived_table_name() if hasattr(cls, "derived_table_name") else getattr(cls, "TABLE_NAME", cls.__name__)


def discover_all() -> List[Type[Migrations]]:
    """
    Discover migration classes for the apps listed in config/apps.cfg (and env),
    importing each file with a unique module name to avoid collisions.
    """
    settings = load_settings()
    project_root = Path(getattr(settings, "project_root", Path.cwd()))
    apps = get_registered_apps()

    classes: List[Type[Migrations]] = []
    seen_keys: Set[Tuple[str, str]] = set()

    for app, file_path in _migration_files(project_root, apps):
        mod_name = _unique_mod_name(app, file_path)

        # Ensure a fresh load
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
                app_name = getattr(attr, "APP_NAME", app or "core")
                tbl_name = _derived_table_name(attr)
                key = (app_name, tbl_name)
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                classes.append(attr)

    def _order_key(cls: Type[Migrations]):
        idx = int(getattr(cls, "ORDER_INDEX", 0))
        app_name = getattr(cls, "APP_NAME", "core")
        tbl_name = _derived_table_name(cls)
        return (idx, app_name, tbl_name)

    classes.sort(key=_order_key)
    return classes
