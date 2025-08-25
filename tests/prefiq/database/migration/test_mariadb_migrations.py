# tests/prefiq/database/migration/test_mariadb_migrations.py
from __future__ import annotations
import socket
import asyncio
import pytest

from prefiq.core.application import Application
from prefiq.providers.config_provider import ConfigProvider
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
    # MariaDB/MySQL: check current DB (DATABASE()) for 'migrations' table
    return (
        "SELECT 1 "
        "FROM information_schema.tables "
        "WHERE table_schema = DATABASE() AND table_name = 'migrations' "
        "LIMIT 1"
    )


def _first_value(row):
    try:
        if isinstance(row, (list, tuple)):
            return row[0]
        if hasattr(row, "__getitem__") and not isinstance(row, (str, bytes, bytearray)):
            try:
                return row[0]
            except (ValueError, TypeError):
                pass
        if hasattr(row, "keys"):
            for _, v in row.items():
                return v
    except (ValueError, TypeError):
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
        except (ValueError, TypeError):
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
            except (ValueError, TypeError):
                pass
    return bool(_first_value(row))


def _table_exists(engine) -> bool:
    try:
        return _table_exists_sync(engine)
    except (ValueError, TypeError):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(_table_exists_async(engine))


@pytest.mark.mariadb
def test_mariadb_migrations_table_exists(engine_swap, mysql_cli):
    # Optional: skip cleanly if mariadb driver not installed
    try:
        import mariadb  # noqa: F401
    except (ValueError, TypeError):
        pytest.skip("mariadb driver not installed")

    host = mysql_cli["host"]
    port = int(mysql_cli["port"])
    user = mysql_cli["user"]
    password = mysql_cli["password"]
    db = mysql_cli["db"]
    mode = mysql_cli["mode"] if mysql_cli["mode"] in ("sync", "async") else "sync"

    if not _port_open(host, port):
        pytest.skip(f"MariaDB not reachable at {host}:{port}")

    with engine_swap(
        DB_ENGINE="mariadb",
        DB_MODE=mode,
        DB_HOST=host,
        DB_PORT=str(port),
        DB_USER=user,
        DB_PASS=password,
        DB_NAME=db,
    ):
        app = Application.get_app()
        app._providers.clear(); app._services.clear(); app._booted = False  # type: ignore[attr-defined]
        app.register(ConfigProvider)
        app.register(DatabaseProvider)
        app.register(MigrationProvider)
        app.boot()

        eng = get_engine()
        assert _table_exists(eng), "migrations table missing on MariaDB"
