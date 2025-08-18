from typing import Callable, Any, Iterable
from prefiq.database.schemas.blueprint import TableBlueprint
from prefiq.database.connection_manager import get_engine
from prefiq.database.dialects.registry import get_dialect

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

# ----------------------- NEW: Index helpers -----------------------

def createIndex(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    """
    Create an index on `table_name` for the given columns.
    Dialect rules:
      - SQLite: CREATE INDEX IF NOT EXISTS idx ON "table" ("col"...)
      - MySQL/MariaDB: CREATE INDEX `idx` ON `table` (`col`...)
      - Postgres: CREATE INDEX IF NOT EXISTS idx ON "table" ("col"...)
    """
    d = get_dialect()
    eng = get_engine()
    dname = (getattr(d, "name", "") or "").lower()

    tname = d.quote_ident(table_name)
    iname = d.quote_ident(index_name)
    cols = ", ".join(d.quote_ident(c) for c in columns)

    if dname in ("sqlite", "postgres", "postgresql"):
        sql = f"CREATE INDEX IF NOT EXISTS {iname} ON {tname} ({cols});"
    else:
        # MySQL/MariaDB have no IF NOT EXISTS for CREATE INDEX
        sql = f"CREATE INDEX {iname} ON {tname} ({cols});"

    sql_norm, _ = d.normalize_params(sql, None)
    eng.execute(sql_norm)

def dropIndexIfExists(table_name: str, index_name: str) -> None:
    """
    Drop an index if it exists.
    Dialect rules:
      - SQLite: DROP INDEX IF EXISTS "idx";
      - MySQL/MariaDB: DROP INDEX `idx` ON `table`;
      - Postgres: DROP INDEX IF EXISTS "idx";
    """
    d = get_dialect()
    eng = get_engine()
    dname = (getattr(d, "name", "") or "").lower()

    tname = d.quote_ident(table_name)
    iname = d.quote_ident(index_name)

    if dname in ("sqlite", "postgres", "postgresql"):
        sql = f"DROP INDEX IF EXISTS {iname};"
    else:
        # MySQL/MariaDB require table name in DROP INDEX
        sql = f"DROP INDEX {iname} ON {tname};"

    sql_norm, _ = d.normalize_params(sql, None)
    eng.execute(sql_norm)
