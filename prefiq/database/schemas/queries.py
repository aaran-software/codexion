# prefiq/database/schemas/queries.py
from __future__ import annotations
from typing import Any, Optional, Tuple
from prefiq.database.schemas.router import impl

_insert, _update, _delete, _select_one, _select_all, _count = (
    impl()[2].insert,
    impl()[2].update,
    impl()[2].delete,
    impl()[2].select_one,
    impl()[2].select_all,
    impl()[2].count,
)

def insert(table_name: str, values: dict) -> None:
    _insert(table_name, values)

def update(table_name: str, values: dict, where: str, params: tuple) -> None:
    _update(table_name, values, where, params)

def delete(table_name: str, where: str, params: tuple) -> None:
    _delete(table_name, where, params)

def select_one(table_name: str, columns: str, where: str, params: tuple) -> Optional[tuple]:
    return _select_one(table_name, columns, where, params)

def select_all(table_name: str, columns: str = "*", where: Optional[str] = None, params: tuple = ()) -> list[tuple]:
    return _select_all(table_name, columns, where, params)

def count(table_name: str, where: Optional[str] = None, params: tuple = ()) -> int:
    return _count(table_name, where, params)
