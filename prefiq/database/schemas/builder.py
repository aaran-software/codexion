# prefiq/database/schemas/builder.py

from typing import Callable, Any
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

