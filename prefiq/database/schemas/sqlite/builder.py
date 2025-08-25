# prefiq/database/schemas/sqlite/builder.py
from __future__ import annotations
from typing import Callable, Any, Iterable, Sequence

from prefiq.database.schemas.sqlite.blueprint import TableBlueprint, q
from prefiq.database.connection_manager import get_engine

def _as_list(columns: Iterable[str] | str) -> list[str]:
    if isinstance(columns, str):
        return [columns]
    if isinstance(columns, Sequence):
        return [str(c) for c in columns]
    return [str(c) for c in list(columns)]

def create(table_name: str, schema_callback: Callable[[TableBlueprint], Any]) -> None:
    table = TableBlueprint(table_name)
    schema_callback(table)

    eng = get_engine()
    tname = q(table_name)

    # Create table first
    sql = f"CREATE TABLE IF NOT EXISTS {tname} (\n  {table.build_columns()}\n);"
    eng.execute(sql)

    # Then create indexes captured by the blueprint
    for iname, cols in table.index_meta:
        createIndex(table_name, iname, cols)

def dropIfExists(table_name: str) -> None:
    get_engine().execute(f"DROP TABLE IF EXISTS {q(table_name)};")

def createIndex(table_name: str, index_name: str | None, columns: Iterable[str] | str) -> None:
    cols = _as_list(columns)
    # If no name provided, auto-generate a deterministic one
    iname = index_name or f"{table_name}_{'_'.join(cols)}_idx"
    t = q(table_name)
    i = q(iname)
    col_sql = ", ".join(q(c) for c in cols)
    get_engine().execute(f"CREATE INDEX IF NOT EXISTS {i} ON {t} ({col_sql});")

def dropIndexIfExists(index_name: str, table_name: str | None = None) -> None:
    # table_name unused for sqlite
    get_engine().execute(f"DROP INDEX IF EXISTS {q(index_name)};")
