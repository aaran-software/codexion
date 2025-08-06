# cortex/database/schemas/builder.py

from typing import Callable, Any
from cortex.database.schemas.blueprint import TableBlueprint
from cortex.database.connection import db


def create(table_name: str, schema_callback: Callable[[TableBlueprint], Any]) -> None:
    """
    Create a table with the given name and schema using a fluent builder.

    Example:
        create("users", lambda table: [
            table.id(),
            table.string("name"),
            table.timestamps()
        ])
    """
    table = TableBlueprint(table_name)
    schema_callback(table)  # Run the schema definition lambda
    sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n  {table.build_columns()}\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    db.execute(sql)


def dropIfExists(table_name: str) -> None:
    """
    Drop a table if it exists.

    Example:
        dropIfExists("users")
    """
    db.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
