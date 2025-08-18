# prefiq/database/schemas/queries.py
from typing import Any, Optional
from prefiq.database.connection import get_engine

def insert(table_name: str, values: dict) -> None:
    if not values:
        raise ValueError("insert() received empty values")
    cols = ", ".join(f"`{k}`" for k in values)
    ph  = ", ".join(["%s"] * len(values))
    sql = f"INSERT INTO `{table_name}` ({cols}) VALUES ({ph})"
    get_engine().execute(sql, tuple(values.values()))

def update(table_name: str, values: dict, where: str, params: tuple) -> None:
    if not values:
        raise ValueError("update() received empty values")
    set_clause = ", ".join(f"`{k}` = %s" for k in values)
    sql = f"UPDATE `{table_name}` SET {set_clause} WHERE {where}"
    get_engine().execute(sql, tuple(values.values()) + params)

def delete(table_name: str, where: str, params: tuple) -> None:
    sql = f"DELETE FROM `{table_name}` WHERE {where}"
    get_engine().execute(sql, params)

def select_one(table_name: str, columns: str, where: str, params: tuple) -> Optional[tuple]:
    sql = f"SELECT {columns} FROM `{table_name}` WHERE {where} LIMIT 1"
    return get_engine().fetchone(sql, params)

def select_all(table_name: str, columns: str = "*", where: Optional[str] = None, params: tuple = ()) -> list[tuple]:
    sql = f"SELECT {columns} FROM `{table_name}`" + (f" WHERE {where}" if where else "")
    return get_engine().fetchall(sql, params)

def count(table_name: str, where: Optional[str] = None, params: tuple = ()) -> int:
    sql = f"SELECT COUNT(*) FROM `{table_name}`" + (f" WHERE {where}" if where else "")
    row = get_engine().fetchone(sql, params)
    return row[0] if row else 0
