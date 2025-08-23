from __future__ import annotations
import os
import pytest
from prefiq.core.contracts.base_provider import Application
from prefiq.providers.settings_provider import SettingsProvider
from prefiq.providers.database_provider import DatabaseProvider
from prefiq.providers.migration_provider import MigrationProvider
from prefiq.database.connection import get_engine
import asyncio
import inspect


def _exists_sql(name: str) -> str:
    return "SELECT 1 FROM information_schema.tables WHERE table_name='migrations'"


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


async def _table_exists_async(engine) -> bool:
    sql = _exists_sql(type(engine).__name__)
    if hasattr(engine, "fetchone") and callable(getattr(engine, "fetchone")):
        row = await engine.fetchone(sql)  # type: ignore[misc]
    else:
        cur = await engine.execute(sql)   # type: ignore[misc]
        row = await cur.fetchone()
        if hasattr(cur, "close"):
            try:
                await cur.close()
            except Exception:
                pass
    return bool(_first_value(row))


@pytest.mark.mariadb
def test_mariadb_migrations_table_exists(engine_swap):
    mdb_db = os.getenv("MDB_DB")
    mdb_user = os.getenv("MDB_USER")
    mdb_pass = os.getenv("MDB_PASS")
    if not all([mdb_db, mdb_user, mdb_pass]):
        pytest.skip("MDB_DB/MDB_USER/MDB_PASS not set")

    with engine_swap(
        DB_ENGINE="mariadb",
        DB_MODE="async",
        DB_HOST=os.getenv("MDB_HOST", "localhost"),
        DB_PORT=os.getenv("MDB_PORT", "3306"),
        DB_USER=mdb_user,
        DB_PASS=mdb_pass,
        DB_NAME=mdb_db,
    ):
        app = Application.get_app()
        app._providers.clear(); app._services.clear(); app._booted = False  # type: ignore
        app.register(SettingsProvider)
        app.register(DatabaseProvider)
        app.register(MigrationProvider)
        app.boot()

        eng = get_engine()
        # run the async check
        asyncio.run(_table_exists_async(eng))
        assert asyncio.run(_table_exists_async(eng)), "migrations table missing on MariaDB"
