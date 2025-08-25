from __future__ import annotations
import asyncio
import inspect
from typing import Callable, Any, Iterable

from prefiq.database.schemas.postgres.blueprint import TableBlueprint, q
from prefiq.database.connection_manager import get_engine


# ── small awaitable adapter (works for sync/async engines) ──────────────────

def _run(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    # Already inside a running loop; spin a quick task and wait
    return _in_loop(coro)

def _in_loop(coro):
    # Fire-and-wait helper when a loop exists
    fut = asyncio.ensure_future(coro)
    loop = asyncio.get_running_loop()
    return loop.run_until_complete(fut)

def _call(fn: Callable, *args, **kwargs):
    res = fn(*args, **kwargs)
    if inspect.isawaitable(res):
        return _run(res)
    return res


# ── DDL helpers ─────────────────────────────────────────────────────────────

def create(table_name: str, schema_callback: Callable[[TableBlueprint], Any]) -> None:
    table = TableBlueprint(table_name)
    schema_callback(table)
    eng = get_engine()

    tname = q(table_name)
    sql = f"CREATE TABLE IF NOT EXISTS {tname} (\n  {table.build_columns()}\n);"
    _call(eng.execute, sql)

    # Post-create indexes (safer than inline; can be concurrent if you later add it)
    for idx_name, cols in table.index_meta:
        createIndex(table_name, idx_name, cols)

def dropIfExists(table_name: str) -> None:
    _call(get_engine().execute, f"DROP TABLE IF EXISTS {q(table_name)};")

def createIndex(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    # Note: Postgres 'CREATE INDEX IF NOT EXISTS' exists and does not need 'ON table' for DROP.
    idx = q(index_name)
    t = q(table_name)
    cols = ", ".join(q(c) for c in columns)
    sql = f"CREATE INDEX IF NOT EXISTS {idx} ON {t} ({cols});"
    try:
        _call(get_engine().execute, sql)
    except Exception as e:
        # Some drivers may wrap errors differently; keep permissive behavior
        msg = str(e).lower()
        if "already exists" in msg:
            return
        raise

def dropIndexIfExists(index_name: str, table_name: str | None = None) -> None:
    # In Postgres, DROP INDEX does not take ON <table>; it drops the named index.
    # We ignore table_name; it’s here for API parity with other builders.
    _call(get_engine().execute, f"DROP INDEX IF EXISTS {q(index_name)};")
