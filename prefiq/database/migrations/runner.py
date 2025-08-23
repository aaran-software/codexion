# prefiq/database/migrations/runner.py
from __future__ import annotations

import datetime
import inspect
from typing import Any

from prefiq.database.connection_manager import get_engine
from prefiq.database.migrations.base import Migrations
from prefiq.database.migrations.discover import discover_all
from prefiq.database.migrations.hashing import compute_callable_hash
from prefiq.database.schemas.builder import ensure_migrations_table
from prefiq.database.schemas.queries import insert, select_all
from prefiq.database.dialects.registry import get_dialect

PROTECTED_TABLES = {"migrations"}


def _engine():
    return get_engine()


def _await(x: Any) -> Any:
    if inspect.isawaitable(x) or inspect.iscoroutine(x):
        import asyncio
        return asyncio.run(x)
    return x


def _applied_map():
    """
    {(app, name): hash}
    """
    rows = select_all("migrations", columns="app, name, hash") or []
    return {(r[0], r[1]): (r[2] or "") for r in rows}


def _record(app: str, name: str, index: int, h: str) -> None:
    insert(
        "migrations",
        {
            "app": app,
            "name": name,
            "order_index": index,
            "hash": h,
            "created_at": datetime.datetime.now(datetime.UTC),
            "updated_at": datetime.datetime.now(datetime.UTC),
        },
    )


def migrate_all() -> None:
    # 1) ensure meta table
    ensure_migrations_table()

    # 2) figure out what's already applied (by hash)
    applied = _applied_map()

    # 3) discover classes and apply in ORDER_INDEX
    for i, cls in enumerate(discover_all()):  # -> List[type[Migrations]]
        app = getattr(cls, "APP_NAME", "core")
        # prefer base helper if present; else fall back to TABLE_NAME/class name
        name = (
            cls.derived_table_name()
            if hasattr(cls, "derived_table_name")
            else getattr(cls, "TABLE_NAME", cls.__name__)
        )
        index = int(getattr(cls, "ORDER_INDEX", i))
        h = compute_callable_hash(cls.up)  # hash the logic we actually run

        if (app, name) in applied:
            if applied[(app, name)] == h:
                print(f"🟡 Skipping {app}.{name} (already applied)")
            else:
                print(f"⚠️  {app}.{name} drift detected; recorded hash differs; skipping.")
            continue

        print(f"✅ Applying {app}.{name} ...")
        inst: Migrations = cls()
        inst.up()
        _record(app, name, index, h)


def drop_all() -> None:
    """
    Danger: drops all tables except the protected list.
    """
    eng = _engine()
    d = get_dialect()
    rows = _await(eng.fetchall(d.list_tables_sql()))
    for (table_name,) in rows:
        if table_name in PROTECTED_TABLES:
            print(f"🛡️  Skipping protected table: {table_name}")
            continue
        qname = d.quote_ident(table_name)
        print(f"🗑️  Dropping table: {table_name}")
        _await(eng.execute(f"DROP TABLE IF EXISTS {qname};"))
