from __future__ import annotations
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
    # Postgres-robust existence check (avoids schema quoting issues)
    return "SELECT to_regclass('public.migrations')"


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
def test_postgres_migrations_table_exists(engine_swap, pg_cli):
    if not pg_cli:
        pytest.skip("Pass --pg-db (and optionally --pg-user/--pg-pass/--pg-host/--pg-port) to run this test")

    if not _port_open(pg_cli["host"], pg_cli["port"]):
        pytest.skip(f"Postgres not reachable at {pg_cli['host']}:{pg_cli['port']}")

    mode = pg_cli["mode"] if pg_cli["mode"] in ("sync", "async") else "sync"

    with engine_swap(
        DB_ENGINE="postgres",
        DB_MODE=mode,
        DB_HOST=pg_cli["host"],
        DB_PORT=str(pg_cli["port"]),
        DB_USER=pg_cli["user"],
        DB_PASS=pg_cli["password"],
        DB_NAME=pg_cli["db"],
    ):
        app = Application.get_app()
        app._providers.clear(); app._services.clear(); app._booted = False  # type: ignore[attr-defined]
        app.register(SettingsProvider)
        app.register(DatabaseProvider)
        app.register(MigrationProvider)
        app.boot()

        eng = get_engine()
        assert _table_exists(eng), "migrations table missing on Postgres"
