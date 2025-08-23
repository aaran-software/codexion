# prefiq/database/migrations/rollback.py
from __future__ import annotations

from typing import Iterable, Optional

from prefiq.database.migrations.discover import discover_all
from prefiq.database.migrations.base import Migrations
from prefiq.database.schemas import queries as q  # module import so tests can monkeypatch
from prefiq.log.logger import get_logger

log = get_logger("prefiq.migrate")

def _iter_unique_classes() -> Iterable[type[Migrations]]:
    """Yield discovered migration classes, de-duplicated by (APP_NAME, name)."""
    seen: set[tuple[str, str]] = set()
    for cls in discover_all():
        app = getattr(cls, "APP_NAME", "core")
        name = (
            cls.derived_table_name()
            if hasattr(cls, "derived_table_name")
            else getattr(cls, "TABLE_NAME", cls.__name__)
        )
        key = (app, name)
        if key in seen:
            continue
        seen.add(key)
        yield cls

def _find_class(app: str, name: str) -> Optional[type[Migrations]]:
    for cls in _iter_unique_classes():
        c_app = getattr(cls, "APP_NAME", "core")
        c_name = (
            cls.derived_table_name()
            if hasattr(cls, "derived_table_name")
            else getattr(cls, "TABLE_NAME", cls.__name__)
        )
        if (c_app, c_name) == (app, name):
            return cls
    return None

def rollback(step: int = 1) -> None:
    """
    Roll back the last `step` migrations by order_index (highest first).
    - Uses queries module so pytest monkeypatches take effect.
    - Tolerates duplicate discoveries.
    """
    # read applied rows; columns are monkeypatched in tests
    rows = q.select_all("migrations", columns="app, name, order_index") or []
    if not rows:
        print("ℹ️  No migrations to rollback.")
        return

    # Sort by order_index ascending then take from end (highest order last applied)
    # Rows are tuples (app, name, order_index)
    rows_sorted = sorted(rows, key=lambda r: (int(r[2]), r[0], r[1]))
    to_rollback = list(reversed(rows_sorted))[: max(0, int(step))]

    if not to_rollback:
        print("ℹ️  No migrations to rollback.")
        return

    for app, name, _idx in to_rollback:
        cls = _find_class(app, name)
        if cls is None:
            # If class is missing, still remove the record to unblock future runs.
            log.warning("rollback_class_missing", extra={"app": app, "name": name})
        else:
            # Call down() on the class
            inst: Migrations = cls()
            inst.down()

        # Remove the record
        q.delete("migrations", "app = ? AND name = ?", (app, name))
        print(f"↩️  Rolled back {app}.{name}")
