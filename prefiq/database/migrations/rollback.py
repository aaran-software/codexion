# prefiq/database/migrations/rollback.py

from __future__ import annotations
import inspect
from typing import Optional, Type

from prefiq.database.schemas.queries import select_all, delete
from prefiq.database.migrations.discover import discover_all
from prefiq.database.migrations.base import Migrations

PROTECTED_MIGRATIONS = {"core": ["migrations"]}

def _is_awaitable(x) -> bool:
    return inspect.isawaitable(x) or inspect.iscoroutine(x)

def _await(x):
    if _is_awaitable(x):
        import asyncio
        return asyncio.run(x)
    return x

def is_protected(app: str, name: str) -> bool:
    return name in PROTECTED_MIGRATIONS.get(app, [])

def _find_class(app: str, name: str) -> Optional[Type[Migrations]]:
    for cls in discover_all():
        if getattr(cls, "APP_NAME", "core") == app and getattr(cls, "TABLE_NAME", cls.__name__) == name:
            return cls
    return None

def rollback(step: int = 1):
    """
    Roll back the last `step` migrations (reverse order), calling class.down() when present.
    """
    applied = select_all("migrations", columns="app, name, order_index")
    if not applied:
        print("ℹ️  No migrations to rollback.")
        return

    # Newest-first
    applied.sort(key=lambda x: x[2], reverse=True)

    rolled_back = 0
    for app, name, _index in applied[:step]:
        if is_protected(app, name):
            print(f"🛑 Skipping protected migration: {app}.{name}")
            continue

        cls = _find_class(app, name)
        if cls is None:
            print(f"⚠️  Cannot find migration class for {app}.{name}. Skipping.")
            continue

        if not hasattr(cls, "down"):
            print(f"⚠️  Migration {app}.{name} has no `down()` method.")
            continue

        print(f"⏪ Rolling back {app}.{name} ...")
        _await(cls.down())
        delete("migrations", "app = %s AND name = %s", (app, name))
        rolled_back += 1

    if rolled_back:
        print(f"✅ Rolled back {rolled_back} migration(s).")
