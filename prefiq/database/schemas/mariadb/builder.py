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

# snake_case alias for legacy imports
def drop_if_exists(table_name: str) -> None:
    return dropIfExists(table_name)

# ----------------------- Index helpers -----------------------

def createIndex(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    """
    Create an index on `table_name` for the given columns.
      - SQLite/Postgres: CREATE INDEX IF NOT EXISTS idx ON "table" ("col"...)
      - MySQL/MariaDB:   CREATE INDEX `idx` ON `table` (`col`...) (idempotent via error swallow)
    """
    d = get_dialect()
    eng = get_engine()
    dname = _dialect_name_lower()

    tname = d.quote_ident(table_name)
    iname = d.quote_ident(index_name)
    cols = ", ".join(d.quote_ident(c) for c in columns)

    if dname in ("sqlite", "postgres", "postgresql"):
        sql = f"CREATE INDEX IF NOT EXISTS {iname} ON {tname} ({cols});"
        sql_norm, _ = d.normalize_params(sql, None)
        eng.execute(sql_norm)
        return

    # MySQL/MariaDB (no IF NOT EXISTS) → ignore duplicate
    sql = f"CREATE INDEX {iname} ON {tname} ({cols});"
    sql_norm, _ = d.normalize_params(sql, None)
    try:
        eng.execute(sql_norm)
    except Exception as e:
        msg = str(e).lower()
        if ("duplicate key name" in msg) or ("errno 1061" in msg) or ("already exists" in msg):
            return  # idempotent no-op
        raise

def dropIndexIfExists(table_name: str, index_name: str) -> None:
    """
    Drop an index if it exists.
      - SQLite/Postgres: DROP INDEX IF EXISTS "idx";
      - MySQL/MariaDB:   DROP INDEX `idx` ON `table`; (ignore missing)
    """
    d = get_dialect()
    eng = get_engine()
    dname = _dialect_name_lower()

    tname = d.quote_ident(table_name)
    iname = d.quote_ident(index_name)

    if dname in ("sqlite", "postgres", "postgresql"):
        sql = f"DROP INDEX IF EXISTS {iname};"
        sql_norm, _ = d.normalize_params(sql, None)
        eng.execute(sql_norm)
        return

    sql = f"DROP INDEX {iname} ON {tname};"
    sql_norm, _ = d.normalize_params(sql, None)
    try:
        eng.execute(sql_norm)
    except Exception as e:
        msg = str(e).lower()
        # Common “missing index” shapes
        if ("doesn't exist" in msg) or ("does not exist" in msg) or ("errno 1091" in msg):
            return
        raise

# snake_case aliases
def create_index(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    return createIndex(table_name, index_name, columns)

def drop_index_if_exists(table_name: str, index_name: str) -> None:
    return dropIndexIfExists(table_name, index_name)
