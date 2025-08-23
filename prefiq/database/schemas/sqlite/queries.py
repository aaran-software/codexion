# prefiq/database/schemas/sqlite/queries.py
from __future__ import annotations
from typing import Any, Optional, Tuple
import inspect

from prefiq.database.connection_manager import get_engine

def q(name: str) -> str:
    # minimal identifier quoting for SQLite
    return f"\"{name}\""

# --- internal helpers to be compatible with both real engines and test fakes ---

def _call_with_optional_params(method: Any, sql: str, params: Tuple[Any, ...] | list[Any] | None):
    """
    Call an engine method that may or may not accept a 'params' argument.
    Tries (sql, params) first if supported; otherwise falls back to (sql).
    """
    try:
        sig = inspect.signature(method)
        # Count user-facing parameters (exclude 'self')
        num_params = len(sig.parameters)
        # Most engines expose method(self, sql[, params])
        if num_params >= 2:
            return method(sql, params or ())
        else:
            return method(sql)
    except (TypeError, ValueError):
        # If introspection fails or call signature mismatches, try best-effort fallbacks
        try:
            return method(sql, params or ())
        except TypeError:
            return method(sql)

def _exec(sql: str, params: Tuple[Any, ...] = ()) -> None:
    eng = get_engine()
    method = getattr(eng, "execute", None)
    if method is None:
        raise RuntimeError("Engine has no 'execute' method")
    _call_with_optional_params(method, sql, params)

def _fetchone(sql: str, params: Tuple[Any, ...] = ()) -> Optional[tuple]:
    eng = get_engine()
    method = getattr(eng, "fetchone", None)
    if method is None:
        # fallback: fetchall and take first
        rows = _fetchall(sql, params)
        return rows[0] if rows else None
    return _call_with_optional_params(method, sql, params)

def _fetchall(sql: str, params: Tuple[Any, ...] = ()) -> list[tuple]:
    eng = get_engine()
    method = getattr(eng, "fetchall", None)
    if method is None:
        raise RuntimeError("Engine has no 'fetchall' method")
    out = _call_with_optional_params(method, sql, params)
    return out or []


# --- public CRUD api used by tests and code ---

def insert(table_name: str, values: dict) -> None:
    if not values:
        raise ValueError("insert() received empty values")
    tname = q(table_name)
    cols = ", ".join(q(k) for k in values.keys())
    ph   = ", ".join(["?"] * len(values))
    sql = f"INSERT INTO {tname} ({cols}) VALUES ({ph})"
    _exec(sql, tuple(values.values()))

def update(table_name: str, values: dict, where: str, params: tuple) -> None:
    if not values:
        raise ValueError("update() received empty values")
    tname = q(table_name)
    set_clause = ", ".join(f"{q(k)} = ?" for k in values.keys())
    sql = f"UPDATE {tname} SET {set_clause} WHERE {where}"
    _exec(sql, tuple(values.values()) + (params or ()))

def delete(table_name: str, where: str, params: tuple) -> None:
    tname = q(table_name)
    sql = f"DELETE FROM {tname} WHERE {where}"
    _exec(sql, params or ())

def select_one(table_name: str, columns: str, where: str, params: tuple) -> Optional[tuple]:
    tname = q(table_name)
    sql = f"SELECT {columns} FROM {tname} WHERE {where} LIMIT 1"
    return _fetchone(sql, params or ())

def select_all(table_name: str, columns: str = "*", where: Optional[str] = None, params: tuple = ()) -> list[tuple]:
    tname = q(table_name)
    sql = f"SELECT {columns} FROM {tname}" + (f" WHERE {where}" if where else "")
    return _fetchall(sql, params or ())

def count(table_name: str, where: Optional[str] = None, params: tuple = ()) -> int:
    tname = q(table_name)
    sql = f"SELECT COUNT(*) FROM {tname}" + (f" WHERE {where}" if where else "")
    row = _fetchone(sql, params or ())
    return int(row[0]) if row else 0
