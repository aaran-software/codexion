# prefiq/database/schemas/sqlite/queries.py
from __future__ import annotations
from typing import Any, Optional, Tuple
from prefiq.database.connection_manager import get_engine

def q(name: str) -> str:
    return f"\"{name}\""

def insert(table_name: str, values: dict) -> None:
    if not values:
        raise ValueError("insert() received empty values")
    tname = q(table_name)
    cols = ", ".join(q(k) for k in values)
    ph  = ", ".join(["?"] * len(values))
    sql = f"INSERT INTO {tname} ({cols}) VALUES ({ph})"
    get_engine().execute(sql, tuple(values.values()))

def update(table_name: str, values: dict, where: str, params: tuple) -> None:
    if not values:
        raise ValueError("update() received empty values")
    tname = q(table_name)
    set_clause = ", ".join(f"{q(k)} = ?" for k in values)
    sql = f"UPDATE {tname} SET {set_clause} WHERE {where}"
    get_engine().execute(sql, tuple(values.values()) + params)

def delete(table_name: str, where: str, params: tuple) -> None:
    tname = q(table_name)
    sql = f"DELETE FROM {tname} WHERE {where}"
    get_engine().execute(sql, params)

def select_one(table_name: str, columns: str, where: str, params: tuple) -> Optional[tuple]:
    tname = q(table_name)
    sql = f"SELECT {columns} FROM {tname} WHERE {where} LIMIT 1"
    return get_engine().fetchone(sql, params)

def select_all(table_name: str, columns: str = "*", where: Optional[str] = None, params: tuple = ()) -> list[tuple]:
    tname = q(table_name)
    sql = f"SELECT {columns} FROM {tname}" + (f" WHERE {where}" if where else "")
    return get_engine().fetchall(sql, params)

def count(table_name: str, where: Optional[str] = None, params: tuple = ()) -> int:
    tname = q(table_name)
    sql = f"SELECT COUNT(*) FROM {tname}" + (f" WHERE {where}" if where else "")
    row = get_engine().fetchone(sql, params)
    return row[0] if row else 0
