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
    # default to public schema
    return "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='migrations'"


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
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(_table_exists_async(engine))


@pytest.mark.postgres
def test_postgres_migrations_table_exists(engine_swap):
    # STRICTLY use PG_* for this test to avoid conftest’s SQLite env.
    pg_db = os.getenv("PG_DB")
    pg_user = os.getenv("PG_USER", "postgres")  # sensible default user
    pg_pass = os.getenv("PG_PASS", "")          # allow trust/peer setups
    pg_host = os.getenv("PG_HOST", "127.0.0.1")
    pg_port = int(os.getenv("PG_PORT", "5432"))

    if not pg_db:
        pytest.skip("Set PG_DB (and optionally PG_USER/PG_PASS) to run Postgres migration test")

    if not _port_open(pg_host, pg_port):
        pytest.skip(f"Postgres not reachable at {pg_host}:{pg_port}")

    mode = os.getenv("PG_MODE", "sync").lower()
    if mode not in ("sync", "async"):
        mode = "sync"

    with engine_swap(
        DB_ENGINE="postgres",
        DB_MODE=mode,
        DB_HOST=pg_host,
        DB_PORT=str(pg_port),
        DB_USER=pg_user,
        DB_PASS=pg_pass,
        DB_NAME=pg_db,
    ):
        app = Application.get_app()
        app._providers.clear(); app._services.clear(); app._booted = False  # type: ignore[attr-defined]
        app.register(SettingsProvider)
        app.register(DatabaseProvider)
        app.register(MigrationProvider)
        app.boot()

        eng = get_engine()
        assert _table_exists(eng), "migrations table missing on Postgres"
