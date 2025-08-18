# prefiq/database/schemas/builder.py
from typing import Callable, Any
from prefiq.database.schemas.blueprint import TableBlueprint
from prefiq.database.connection import get_engine

def create(table_name: str, schema_callback: Callable[[TableBlueprint], Any]) -> None:
    table = TableBlueprint(table_name)
    schema_callback(table)
    sql = (
        f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n  {table.build_columns()}\n)"
        " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    )
    get_engine().execute(sql)  # <-- call the engine

def dropIfExists(table_name: str) -> None:
    get_engine().execute(f"DROP TABLE IF EXISTS `{table_name}`;")  # <-- engine
