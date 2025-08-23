# prefiq/database/schemas/queries.py

from __future__ import annotations
from typing import Optional
from prefiq.database.schemas.router import impl

def _qry():
    # Resolve on each call to respect engine swaps
    return impl()[2]

def insert(table_name: str, values: dict) -> None:
    _qry().insert(table_name, values)

def update(table_name: str, values: dict, where: str, params: tuple) -> None:
    _qry().update(table_name, values, where, params)

def delete(table_name: str, where: str, params: tuple) -> None:
    _qry().delete(table_name, where, params)

def select_one(table_name: str, columns: str, where: str, params: tuple) -> Optional[tuple]:
    return _qry().select_one(table_name, columns, where, params)

def select_all(table_name: str, columns: str = "*", where: Optional[str] = None, params: tuple = ()) -> list[tuple]:
    return _qry().select_all(table_name, columns, where, params)

def count(table_name: str, where: Optional[str] = None, params: tuple = ()) -> int:
    return _qry().count(table_name, where, params)
