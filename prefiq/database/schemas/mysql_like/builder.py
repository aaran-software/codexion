# prefiq/database/schemas/mysql_like/builder.py
from __future__ import annotations
from typing import Callable, Any, Iterable

from prefiq.database.schemas.mysql_like.blueprint import TableBlueprint, q
from prefiq.database.connection_manager import get_engine

ENGINE_SUFFIX = " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"

def create(table_name: str, schema_callback: Callable[[TableBlueprint], Any]) -> None:
    table = TableBlueprint(table_name)
    schema_callback(table)
    eng = get_engine()
    tname = q(table_name)
    sql = f"CREATE TABLE IF NOT EXISTS {tname} (\n  {table.build_columns()}\n){ENGINE_SUFFIX}"
    eng.execute(sql)

def dropIfExists(table_name: str) -> None:
    eng = get_engine()
    eng.execute(f"DROP TABLE IF EXISTS {q(table_name)};")

def createIndex(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    eng = get_engine()
    cols = ", ".join(q(c) for c in columns)
    sql = f"CREATE INDEX {q(index_name)} ON {q(table_name)} ({cols});"
    try:
        eng.execute(sql)
    except Exception as e:
        msg = str(e).lower()
        if ("duplicate key name" in msg) or ("errno 1061" in msg) or ("already exists" in msg):
            return
        raise

def dropIndexIfExists(table_name: str, index_name: str) -> None:
    eng = get_engine()
    sql = f"DROP INDEX {q(index_name)} ON {q(table_name)};"
    try:
        eng.execute(sql)
    except Exception as e:
        msg = str(e).lower()
        if ("doesn't exist" in msg) or ("does not exist" in msg) or ("errno 1091" in msg):
            return
        raise
