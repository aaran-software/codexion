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
from prefiq.database.dialects.registry import get_dialect
from prefiq.database.schemas import queries as q

PROTECTED_TABLES = {"migrations"}


def _engine():
    return get_engine()


def _await(x: Any) -> Any:
    if inspect.isawaitable(x) or inspect.iscoroutine(x):
        import asyncio
        return asyncio.run(x)
    return x


def _applied_map() -> dict[tuple[str, str], str]:
    """
    {(app, name): hash}
    """
    rows = q.select_all("migrations", columns="app, name, hash") or []
    return {(r[0], r[1]): (r[2] or "") for r in rows}


def _record(app: str, name: str, index: int, h: str) -> None:
    now = datetime.datetime.now(datetime.UTC)
    q.insert(
        "migrations",
        {
            "app": app,
            "name": name,
            "order_index": index,
            "hash": h,
            "created_at": now,
            "updated_at": now,
        },
    )



def migrate_all() -> None:
    ensure_migrations_table()

    applied = _applied_map()
    seen: set[tuple[str, str]] = set(applied.keys())  # ← track during this run

    for i, cls in enumerate(discover_all()):
        app = getattr(cls, "APP_NAME", "core")
        name = (
            cls.derived_table_name()
            if hasattr(cls, "derived_table_name")
            else getattr(cls, "TABLE_NAME", cls.__name__)
        )
        index = int(getattr(cls, "ORDER_INDEX", i))
        h = compute_callable_hash(cls.up)
        key = (app, name)

        if key in seen:
            if applied.get(key) == h:
                print(f"🟡 Skipping {app}.{name} (already applied)")
            else:
                print(f"⚠️  {app}.{name} drift detected; recorded hash differs; skipping.")
            continue

        print(f"✅ Applying {app}.{name} ...")
        inst: Migrations = cls()
        inst.up()
        _record(app, name, index, h)
        seen.add(key)  # ← mark immediately


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
