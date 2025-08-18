# prefiq/database/schemas/queries.py

from typing import Any, Optional, Tuple
from prefiq.database.connection_manager import get_engine
from prefiq.database.dialects.registry import get_dialect

def _do(sql: str, params: Tuple[Any, ...] | None, fn):
    d = get_dialect()
    eng = get_engine()
    sql2, p2 = d.normalize_params(sql, params)
    return fn(sql2, p2 or ())

def insert(table_name: str, values: dict) -> None:
    if not values:
        raise ValueError("insert() received empty values")
    d = get_dialect()
    tname = d.quote_ident(table_name)
    cols = ", ".join(d.quote_ident(k) for k in values)
    ph  = ", ".join(["%s"] * len(values))
    sql = f"INSERT INTO {tname} ({cols}) VALUES ({ph})"
    _do(sql, tuple(values.values()), get_engine().execute)

def update(table_name: str, values: dict, where: str, params: tuple) -> None:
    if not values:
        raise ValueError("update() received empty values")
    d = get_dialect()
    tname = d.quote_ident(table_name)
    set_clause = ", ".join(f"{d.quote_ident(k)} = %s" for k in values)
    sql = f"UPDATE {tname} SET {set_clause} WHERE {where}"
    _do(sql, tuple(values.values()) + params, get_engine().execute)

def delete(table_name: str, where: str, params: tuple) -> None:
    d = get_dialect()
    tname = d.quote_ident(table_name)
    sql = f"DELETE FROM {tname} WHERE {where}"
    _do(sql, params, get_engine().execute)

def select_one(table_name: str, columns: str, where: str, params: tuple) -> Optional[tuple]:
    d = get_dialect()
    tname = d.quote_ident(table_name)
    sql = f"SELECT {columns} FROM {tname} WHERE {where} LIMIT 1"
    return _do(sql, params, get_engine().fetchone)

def select_all(table_name: str, columns: str = "*", where: Optional[str] = None, params: tuple = ()) -> list[tuple]:
    d = get_dialect()
    tname = d.quote_ident(table_name)
    sql = f"SELECT {columns} FROM {tname}" + (f" WHERE {where}" if where else "")
    return _do(sql, params, get_engine().fetchall)

def count(table_name: str, where: Optional[str] = None, params: tuple = ()) -> int:
    d = get_dialect()
    tname = d.quote_ident(table_name)
    sql = f"SELECT COUNT(*) FROM {tname}" + (f" WHERE {where}" if where else "")
    row = _do(sql, params, get_engine().fetchone)
    return row[0] if row else 0

