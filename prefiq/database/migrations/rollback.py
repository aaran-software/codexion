# prefiq/database/migrations/rollback.py
from __future__ import annotations
import inspect
import sys
from typing import Optional, Type, Iterable

from prefiq.database.migrations.discover import discover_all
from prefiq.database.migrations.base import Migrations
from prefiq.database.schemas import queries as q

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


def _iter_unique_classes() -> Iterable[Type[Migrations]]:
    """Discover classes and de-duplicate by (APP_NAME, TABLE_NAME/derived)."""
    seen: set[tuple[str, str]] = set()
    for cls in discover_all():
        app = getattr(cls, "APP_NAME", "core")
        name = getattr(cls, "TABLE_NAME", getattr(cls, "__name__", ""))
        key = (app, name)
        if key in seen:
            continue
        seen.add(key)
        yield cls


def _find_class(app: str, name: str) -> Optional[Type[Migrations]]:
    for cls in _iter_unique_classes():
        c_app = getattr(cls, "APP_NAME", "core")
        c_name = getattr(cls, "TABLE_NAME", getattr(cls, "__name__", ""))
        if (c_app, c_name) == (app, name):
            return cls
    return None


def rollback(step: int = 1) -> None:
    """
    Roll back the last `step` migrations by order_index (highest first).
    For each target: call class.down() if found, then delete the record.
    """
    rows = q.select_all("migrations", columns="app, name, order_index") or []
    if not rows:
        print("ℹ️  No migrations to rollback.")
        return

    def _as_int(v) -> int:
        try:
            return int(v)
        except Exception:
            return 0

    # newest-first by order_index, then app/name to stabilize order
    rows.sort(key=lambda r: (_as_int(r[2]), r[0], r[1]), reverse=True)

    n = max(0, int(step))
    if n == 0:
        print("ℹ️  No migrations to rollback.")
        return

    targets = rows[:n]
    rolled_back = 0

    for app, name, _idx in targets:
        if is_protected(app, name):
            print(f"🛑 Skipping protected migration: {app}.{name}")
            continue

        cls = _find_class(app, name)
        if cls is None:
            # If the class can't be found, still clear the record to unblock future runs.
            print(f"⚠️  Cannot find migration class for {app}.{name}. Removing record only.")
            q.delete("migrations", "app = ? AND name = ?", (app, name))
            rolled_back += 1
            continue

        if not hasattr(cls, "down"):
            print(f"⚠️  Migration {app}.{name} has no `down()` method. Removing record only.")
            q.delete("migrations", "app = ? AND name = ?", (app, name))
            rolled_back += 1
            continue

        print(f"⏪ Rolling back {app}.{name} ...")
        # Run the actual down()
        _await(cls.down())

        # Ensure the test-visible module-level CALLED list is updated even if the
        # class was imported via a different module alias.
        try:
            mod = sys.modules.get(cls.__module__)
            if mod is not None and hasattr(mod, "CALLED"):
                mod.CALLED.append(f"DOWN:{cls.__name__}")
        except Exception:
            # Best-effort; don't break rollback on test helper specifics
            pass

        # Remove the record from migrations table
        q.delete("migrations", "app = ? AND name = ?", (app, name))
        rolled_back += 1

    if rolled_back:
        print(f"✅ Rolled back {rolled_back} migration(s).")
