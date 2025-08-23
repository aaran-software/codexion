# prefiq/database/schemas/builder.py
from __future__ import annotations
from typing import Callable, Any, Iterable
from prefiq.database.schemas.router import impl

_create, _dropIfExists, _createIndex, _dropIndexIfExists = (
    impl()[1].create,
    impl()[1].dropIfExists,
    impl()[1].createIndex,
    impl()[1].dropIndexIfExists,
)

def create(table_name: str, schema_callback: Callable[[Any], Any]) -> None:
    _create(table_name, schema_callback)

def dropIfExists(table_name: str) -> None:
    _dropIfExists(table_name)

def drop_if_exists(table_name: str) -> None:  # alias
    _dropIfExists(table_name)

def createIndex(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    _createIndex(table_name, index_name, columns)

def dropIndexIfExists(table_name: str, index_name: str) -> None:
    _dropIndexIfExists(table_name, index_name)

def create_index(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    _createIndex(table_name, index_name, columns)

def drop_index_if_exists(table_name: str, index_name: str) -> None:
    _dropIndexIfExists(table_name, index_name)
