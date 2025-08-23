# prefiq/database/migrations/runner.py

from __future__ import annotations

import datetime
import inspect
import sys
from typing import Any, Type

from prefiq.database.connection_manager import get_engine
from prefiq.database.migrations.discover import discover_all
from prefiq.database.migrations.hashing import compute_file_hash
from prefiq.database.schemas.queries import insert
from prefiq.database.schemas.builder import create
from prefiq.database.schemas.blueprint import TableBlueprint
from prefiq.database.dialects.registry import get_dialect
from prefiq.database.migrations.base import Migrations

PROTECTED_TABLES = {"migrations"}

def _engine():
    return get_engine()

def _is_awaitable(x: Any) -> bool:
    return inspect.isawaitable(x) or inspect.iscoroutine(x)

def _await(x: Any) -> Any:
    if _is_awaitable(x):
        import asyncio
        return asyncio.run(x)
    return x

def _ensure_migrations_table() -> None:
    def _schema(t: TableBlueprint):
        t.id("id")
        t.string("app", 255, nullable=False)
        t.string("name", 255, nullable=False)
        t.integer("order_index", nullable=False, default=0)
        t.string("hash", 255, nullable=False)
        t.datetime("created_at", nullable=False, default="CURRENT_TIMESTAMP")
        t.datetime("updated_at", nullable=False, default="CURRENT_TIMESTAMP")
        t.index("idx_migrations_app", "app")
        t.unique("ux_migrations_app_name", ["app", "name"])
    create("migrations", _schema)

def _module_file_of(cls: Type[Migrations]) -> str:
    mod = sys.modules.get(cls.__module__)
    if not mod or not getattr(mod, "__file__", None):
        raise RuntimeError(f"Cannot resolve file for {cls.__module__}.{cls.__name__}")
    return mod.__file__  # type: ignore[return-value]

def _is_applied(app: str, name: str, hash_: str) -> bool:
    eng = _engine()
    row = _await(eng.fetchone("SELECT hash FROM migrations WHERE app = %s AND name = %s", (app, name)))
    if row:
        if row[0] != hash_:
            print(f"⚠️  {app}.{name} hash differs from recorded hash (file changed since first apply).")
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

def migrate_all() -> None:
    _ensure_migrations_table()
    classes = discover_all()  # List[type[Migrations]]
    for i, cls in enumerate(classes):
        app = getattr(cls, "APP_NAME", "core")
        name = getattr(cls, "TABLE_NAME", cls.__name__)
        order_index = int(getattr(cls, "ORDER_INDEX", i))

        file_path = _module_file_of(cls)
        hash_ = compute_file_hash(file_path)

        if _is_applied(app, name, hash_):
            print(f"🟡 Skipping {app}.{name} (already applied)")
            continue

        print(f"✅ Running {app}.{name} ...")
        _await(cls.up())
        _record_migration(app, name, order_index, hash_)

def drop_all() -> None:
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
