from __future__ import annotations
import os
import socket
import asyncio
import pytest

from prefiq.core.contracts.base_provider import Application
from prefiq.providers.settings_provider import SettingsProvider
from prefiq.providers.database_provider import DatabaseProvider
from prefiq.providers.migration_provider import MigrationProvider
from prefiq.database.connection import get_engine


def _port_open(host: str, port: int, timeout=1.5) -> bool:
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except OSError:
        return False


def _exists_sql() -> str:
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


def _table_exists_sync(engine) -> bool:
    sql = _exists_sql()
    if hasattr(engine, "fetchone") and callable(getattr(engine, "fetchone")):
        row = engine.fetchone(sql)
        return bool(_first_value(row))
    cur = engine.execute(sql)
    try:
        row = cur.fetchone()
    finally:
        try:
            cur.close()
        except Exception:
            pass
    return bool(_first_value(row))


async def _table_exists_async(engine) -> bool:
    sql = _exists_sql()
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


def _table_exists(engine) -> bool:
    try:
        return _table_exists_sync(engine)
    except Exception:
        loop = None
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(_table_exists_async(engine))


@pytest.mark.mariadb
def test_mariadb_migrations_table_exists(engine_swap):
    # STRICTLY use MDB_* for this test to avoid conftest’s SQLite env.
    mdb_db = os.getenv("MDB_DB")
    mdb_user = os.getenv("MDB_USER")
    mdb_pass = os.getenv("MDB_PASS")
    mdb_host = os.getenv("MDB_HOST", "127.0.0.1")
    mdb_port = int(os.getenv("MDB_PORT", "3306"))

    if not all([mdb_db, mdb_user, mdb_pass]):
        pytest.skip("Set MDB_DB/MDB_USER/MDB_PASS to run MariaDB migration test")

    if not _port_open(mdb_host, mdb_port):
        pytest.skip(f"MariaDB not reachable at {mdb_host}:{mdb_port}")

    mode = os.getenv("MDB_MODE", "async").lower()
    if mode not in ("sync", "async"):
        mode = "async"

    with engine_swap(
        DB_ENGINE="mariadb",
        DB_MODE=mode,
        DB_HOST=mdb_host,
        DB_PORT=str(mdb_port),
        DB_USER=mdb_user,
        DB_PASS=mdb_pass,
        DB_NAME=mdb_db,
    ):
        app = Application.get_app()
        app._providers.clear(); app._services.clear(); app._booted = False  # type: ignore[attr-defined]
        app.register(SettingsProvider)
        app.register(DatabaseProvider)
        app.register(MigrationProvider)
        app.boot()

        eng = get_engine()
        assert _table_exists(eng), "migrations table missing on MariaDB"
