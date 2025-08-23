from __future__ import annotations
import asyncio
import inspect
from typing import Callable, Any, Iterable

from prefiq.database.schemas.mysql_like.blueprint import TableBlueprint, q
from prefiq.database.connection_manager import get_engine


def _run(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    # If we're already inside a running loop (e.g., pytest plugins), run in a temp thread/loop.
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


ENGINE_SUFFIX = " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"

def create(table_name: str, schema_callback: Callable[[TableBlueprint], Any]) -> None:
    table = TableBlueprint(table_name)
    schema_callback(table)
    eng = get_engine()
    tname = q(table_name)
    sql = f"CREATE TABLE IF NOT EXISTS {tname} (\n  {table.build_columns()}\n){ENGINE_SUFFIX}"
    _call(eng.execute, sql)

def dropIfExists(table_name: str) -> None:
    eng = get_engine()
    _call(eng.execute, f"DROP TABLE IF EXISTS {q(table_name)};")

def createIndex(table_name: str, index_name: str, columns: Iterable[str]) -> None:
    eng = get_engine()
    cols = ", ".join(q(c) for c in columns)
    sql = f"CREATE INDEX {q(index_name)} ON {q(table_name)} ({cols});"
    try:
        _call(eng.execute, sql)
    except Exception as e:
        msg = str(e).lower()
        if ("duplicate key name" in msg) or ("errno 1061" in msg) or ("already exists" in msg):
            return
        raise

def dropIndexIfExists(table_name: str, index_name: str) -> None:
    eng = get_engine()
    sql = f"DROP INDEX {q(index_name)} ON {q(table_name)};"
    try:
        _call(eng.execute, sql)
    except Exception as e:
        msg = str(e).lower()
        if ("doesn't exist" in msg) or ("does not exist" in msg) or ("errno 1091" in msg):
            return
        raise
