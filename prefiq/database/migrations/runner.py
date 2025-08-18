# =============================================================
# Migration Runner (runner.py)
#
# Applies all pending migrations for all apps.
# Tracks state in `migrations` table using schema builder.
# Works with both sync and async engines.
# =============================================================

from __future__ import annotations

import datetime
import inspect
from typing import Any, Tuple
from pathlib import Path

from prefiq.database.connection_manager import get_engine
from cortex.database.base_tables import m000_migration_table
from prefiq.database.migrations.loader import (
    discover_all_app_migrations,
    resolve_and_load,
)
from prefiq.database.schemas.queries import insert

# Core/system tables that should not be dropped
PROTECTED_TABLES = {"migrations", "tenants", "users"}


# --- small helpers -----------------------------------------------------------

def _engine():
    """Return the current DB engine (sync or async) selected by settings."""
    return get_engine()

def _is_awaitable(x: Any) -> bool:
    return inspect.isawaitable(x) or inspect.iscoroutine(x)

def _await(x: Any) -> Any:
    """Run sync values as-is; await async values safely."""
    if _is_awaitable(x):
        import asyncio
        return asyncio.run(x)
    return x


# --- internal ops ------------------------------------------------------------

def _ensure_migrations_table() -> None:
    # ensure base 'migrations' table exists
    if hasattr(m000_migration_table, "up"):
        m000_migration_table.up()


def _is_applied(app: str, name: str, hash_: str) -> bool:
    eng = _engine()
    row = _await(eng.fetchone(
        "SELECT hash FROM migrations WHERE app = %s AND name = %s",
        (app, name),
    ))

    if row:
        if row[0] != hash_:
            print(f"⚠️  {app}.{name} hash differs from recorded hash (was changed since first apply).")
        return row[0] == hash_
    return False


def _record_migration(app: str, name: str, index: int, hash_: str) -> None:
    insert("migrations", {
        "app": app,
        "name": name,
        "order_index": index,
        "hash": hash_,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow(),
    })


# --- public API --------------------------------------------------------------

def migrate_all() -> None:
    """
    Discover and apply all pending migrations across all apps.
    """
    _ensure_migrations_table()

    apps = discover_all_app_migrations()
    # apps: Dict[str, List[str]] where key = app name, value = ordered migration names

    for app, migration_list in apps.items():
        for i, name in enumerate(migration_list):
            try:
                mod, hash_ = resolve_and_load(app, name)

                if _is_applied(app, name, hash_):
                    print(f"🟡 Skipping {app}.{name} (already applied)")
                    continue

                if not hasattr(mod, "up"):
                    raise AttributeError(f"Migration {name} in {app} has no `up()` function")

                print(f"✅ Running {app}.{name} ...")
                _await(mod.up())
                _record_migration(app, name, i, hash_)

            except Exception as e:
                print(f"❌ Failed to apply {app}.{name}: {e}")
                raise


def drop_all() -> None:
    """
    Drop all tables except the protected set (useful for --fresh).
    """
    eng = _engine()
    rows = _await(eng.fetchall("SHOW TABLES"))

    # rows is typically List[Tuple[str]]
    for (table_name,) in rows:
        if table_name in PROTECTED_TABLES:
            print(f"🛡️  Skipping protected table: {table_name}")
            continue
        print(f"🗑️  Dropping table: {table_name}")
        _await(eng.execute(f"DROP TABLE IF EXISTS `{table_name}`;"))
