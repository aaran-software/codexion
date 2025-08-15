# cortex/database/schemas/queries.py

from typing import Any, Optional
from cortex.database.connection import db


def insert(table_name: str, values: dict) -> None:
    """
    Insert a new row into the given table.
    """
    if not values:
        raise ValueError("insert() received empty values")

    columns = ", ".join(f"`{k}`" for k in values)
    placeholders = ", ".join(["%s"] * len(values))
    sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
    db.execute(sql, tuple(values.values()))


def update(table_name: str, values: dict, where: str, params: tuple) -> None:
    """
    Update rows in a table.

    Example:
        update("users", {"name": "Aaran"}, "id = %s", (5,))
    """
    if not values:
        raise ValueError("update() received empty values")

    set_clause = ", ".join(f"`{k}` = %s" for k in values)
    sql = f"UPDATE `{table_name}` SET {set_clause} WHERE {where}"
    db.execute(sql, tuple(values.values()) + params)


def delete(table_name: str, where: str, params: tuple) -> None:
    """
    Delete rows from a table.

    Example:
        delete("users", "id = %s", (5,))
    """
    sql = f"DELETE FROM `{table_name}` WHERE {where}"
    db.execute(sql, params)


def select_one(table_name: str, columns: str, where: str, params: tuple) -> Optional[tuple]:
    """
    Fetch a single row from a table.

    Example:
        select_one("users", "*", "email = %s", ("a@b.com",))
    """
    sql = f"SELECT {columns} FROM `{table_name}` WHERE {where} LIMIT 1"
    return db.fetchone(sql, params)


def select_all(table_name: str, columns: str = "*", where: Optional[str] = None, params: tuple = ()) -> list[tuple]:
    """
    Fetch all rows from a table.

    Example:
        select_all("users")  # fetches all rows
        select_all("users", "*", "is_active = %s", (True,))
    """
    sql = f"SELECT {columns} FROM `{table_name}`"
    if where:
        sql += f" WHERE {where}"

    return db.fetchall(sql, params)

def count(table_name: str, where: Optional[str] = None, params: tuple = ()) -> int:
    """
    Count rows in a table.

    Example:
        count("users")
        count("users", "is_active = %s", (True,))
    """
    sql = f"SELECT COUNT(*) FROM `{table_name}`"
    if where:
        sql += f" WHERE {where}"
    result = db.fetchone(sql, params)
    return result[0] if result else 0
