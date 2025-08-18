# prefiq/database/schemas/builder.py

from typing import Callable, Any, Iterable
from prefiq.database.schemas.blueprint import TableBlueprint
from prefiq.database.connection_manager import get_engine
from prefiq.database.dialects.registry import get_dialect

__all__ = [
    "create",
    "dropIfExists",
    "drop_if_exists",
    "createIndex",
    "dropIndexIfExists",
    "create_index",
    "drop_index_if_exists",
]

def _dialect_name_lower() -> str:
    d = get_dialect()
    n = getattr(d, "name", None)
    if callable(n):
        try:
            n = n()
        except Exception:
            n = None
    if isinstance(n, str):
        return n.lower()
    return type(d).__name__.lower()

def create(table_name: str, schema_callback: Callable[[TableBlueprint], Any]) -> None:
    table = TableBlueprint(table_name)
    schema_callback(table)
    d = get_dialect()
    tname = d.quote_ident(table_name)
    suffix = d.create_table_suffix()
    sql = f"CREATE TABLE IF NOT EXISTS {tname} (\n  {table.build_columns()}\n){suffix}"
    eng = get_engine()
    sql_norm, _ = d.normalize_params(sql, None)
    eng.execute(sql_norm)

def dropIfExists(table_name: str) -> None:
    d = get_dialect()
    tname = d.quote_ident(table_name)
    sql = f"DROP TABLE IF EXISTS {tname};"
    eng = get_engine()
    sql_norm, _ = d.normalize_params(sql, None)
    eng.execute(sql_norm)

# snake_case alias needed by cortex.m000_migration_table
def drop_if_exists(table_name: str) -> None:
    return dropIfExists(table_name)

# ----------------------- Index helpers -----------------------

def createIndex(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    """
    Create an index on `table_name` for the given columns.
      - SQLite/Postgres: CREATE INDEX IF NOT EXISTS idx ON "table" ("col"...)
      - MySQL/MariaDB:   CREATE INDEX `idx` ON `table` (`col`...)
    """
    d = get_dialect()
    eng = get_engine()
    dname = _dialect_name_lower()

    tname = d.quote_ident(table_name)
    iname = d.quote_ident(index_name)
    cols = ", ".join(d.quote_ident(c) for c in columns)

    if dname in ("sqlite", "postgres", "postgresql"):
        sql = f"CREATE INDEX IF NOT EXISTS {iname} ON {tname} ({cols});"
    else:
        # MySQL/MariaDB have no IF NOT EXISTS in CREATE INDEX
        sql = f"CREATE INDEX {iname} ON {tname} ({cols});"

    sql_norm, _ = d.normalize_params(sql, None)
    eng.execute(sql_norm)

def dropIndexIfExists(table_name: str, index_name: str) -> None:
    """
    Drop an index if it exists.
      - SQLite/Postgres: DROP INDEX IF EXISTS "idx";
      - MySQL/MariaDB:   DROP INDEX `idx` ON `table`;
    """
    d = get_dialect()
    eng = get_engine()
    dname = _dialect_name_lower()

    tname = d.quote_ident(table_name)
    iname = d.quote_ident(index_name)

    if dname in ("sqlite", "postgres", "postgresql"):
        sql = f"DROP INDEX IF EXISTS {iname};"
    else:
        # MySQL/MariaDB require table name for DROP INDEX
        sql = f"DROP INDEX {iname} ON {tname};"

    sql_norm, _ = d.normalize_params(sql, None)
    eng.execute(sql_norm)

# snake_case aliases for convenience
def create_index(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    return createIndex(table_name, index_name, columns)

def drop_index_if_exists(table_name: str, index_name: str) -> None:
    return dropIndexIfExists(table_name, index_name)
