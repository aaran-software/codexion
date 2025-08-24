from __future__ import annotations
from prefiq.core.application import Application
from prefiq.providers.config_provider import ConfigProvider
from prefiq.providers.database_provider import DatabaseProvider
from prefiq.providers.migration_provider import MigrationProvider
from prefiq.database.connection import get_engine
import asyncio
import inspect


def _exists_sql(name: str) -> str:
    return "SELECT name FROM sqlite_master WHERE type='table' AND name='migrations'"


def _first_value(row):
    try:
        if isinstance(row, (list, tuple)):
            return row[0]
        if hasattr(row, "__getitem__") and not isinstance(row, (str, bytes, bytearray)):
            try:
                return row[0]
            except Exception:
                pass
        if hasattr(row, "keys"):
            for _, v in row.items():
                return v
    except Exception:
        pass
    return row


def _table_exists(engine) -> bool:
    sql = _exists_sql(type(engine).__name__)
    if hasattr(engine, "fetchone") and callable(getattr(engine, "fetchone")):
        row = engine.fetchone(sql)
        return bool(_first_value(row))
    cur = engine.execute(sql)
    row = cur.fetchone()
    try:
        cur.close()
    except Exception:
        pass
    return bool(_first_value(row))


def test_sqlite_migrations_table_exists(engine_swap):
    with engine_swap(DB_ENGINE="sqlite", DB_MODE="sync", DB_NAME=":memory:"):
        app = Application.get_app()
        app._providers.clear();
        app._services.clear();
        app._booted = False  # type: ignore
        app.register(ConfigProvider)
        app.register(DatabaseProvider)
        app.register(MigrationProvider)
        app.boot()

        eng = get_engine()
        assert _table_exists(eng), "migrations table missing on SQLite"
