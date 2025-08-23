# prefiq/database/schemas/sqlite/builder.py
from __future__ import annotations
from typing import Callable, Any, Iterable

from prefiq.database.schemas.sqlite.blueprint import TableBlueprint, q
from prefiq.database.connection_manager import get_engine

def create(table_name: str, schema_callback: Callable[[TableBlueprint], Any]) -> None:
    table = TableBlueprint(table_name)
    schema_callback(table)
    eng = get_engine()
    tname = q(table_name)
    sql = f"CREATE TABLE IF NOT EXISTS {tname} (\n  {table.build_columns()}\n);"
    eng.execute(sql)
    # post-create indexes
    for iname, cols in table.index_meta:
        createIndex(table_name, iname, cols)

def dropIfExists(table_name: str) -> None:
    get_engine().execute(f"DROP TABLE IF EXISTS {q(table_name)};")

def createIndex(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    t = q(table_name)
    i = q(index_name)
    cols = ", ".join(q(c) for c in columns)
    get_engine().execute(f"CREATE INDEX IF NOT EXISTS {i} ON {t} ({cols});")

def dropIndexIfExists(index_name: str, table_name: str | None = None) -> None:
    # table unused for sqlite drop
    get_engine().execute(f"DROP INDEX IF EXISTS {q(index_name)};")
