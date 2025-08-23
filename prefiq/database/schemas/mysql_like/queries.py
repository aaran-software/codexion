from __future__ import annotations
import asyncio
import inspect
from typing import Optional
from prefiq.database.connection_manager import get_engine

def q(name: str) -> str:
    return f"`{name}`"

def _run(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    from concurrent.futures import ThreadPoolExecutor

    def _runner():
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    with ThreadPoolExecutor(max_workers=1) as ex:
        return ex.submit(_runner).result()

def _call(meth, *args):
    res = meth(*args)
    if inspect.isawaitable(res):
        return _run(res)
    return res

def insert(table_name: str, values: dict) -> None:
    if not values:
        raise ValueError("insert() received empty values")
    tname = q(table_name)
    cols = ", ".join(q(k) for k in values)
    ph  = ", ".join(["%s"] * len(values))
    sql = f"INSERT INTO {tname} ({cols}) VALUES ({ph})"
    _call(get_engine().execute, sql, tuple(values.values()))

def update(table_name: str, values: dict, where: str, params: tuple) -> None:
    if not values:
        raise ValueError("update() received empty values")
    tname = q(table_name)
    set_clause = ", ".join(f"{q(k)} = %s" for k in values)
    sql = f"UPDATE {tname} SET {set_clause} WHERE {where}"
    _call(get_engine().execute, sql, tuple(values.values()) + params)

def delete(table_name: str, where: str, params: tuple) -> None:
    tname = q(table_name)
    sql = f"DELETE FROM {tname} WHERE {where}"
    _call(get_engine().execute, sql, params)

def select_one(table_name: str, columns: str, where: str, params: tuple) -> Optional[tuple]:
    tname = q(table_name)
    sql = f"SELECT {columns} FROM {tname} WHERE {where} LIMIT 1"
    return _call(get_engine().fetchone, sql, params)

def select_all(table_name: str, columns: str = "*", where: Optional[str] = None, params: tuple = ()) -> list[tuple]:
    tname = q(table_name)
    sql = f"SELECT {columns} FROM {tname}" + (f" WHERE {where}" if where else "")
    return _call(get_engine().fetchall, sql, params)

def count(table_name: str, where: Optional[str] = None, params: tuple = ()) -> int:
    tname = q(table_name)
    sql = f"SELECT COUNT(*) FROM {tname}" + (f" WHERE {where}" if where else "")
    row = _call(get_engine().fetchone, sql, params)
    return row[0] if row else 0
