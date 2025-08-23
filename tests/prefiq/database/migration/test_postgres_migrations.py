from __future__ import annotations
import os
import pytest
from prefiq.core.contracts.base_provider import Application
from prefiq.providers.settings_provider import SettingsProvider
from prefiq.providers.database_provider import DatabaseProvider
from prefiq.providers.migration_provider import MigrationProvider
from prefiq.database.connection import get_engine


def _exists_sql(name: str) -> str:
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


@pytest.mark.postgres
def test_postgres_migrations_table_exists(engine_swap):
    # Require credentials; skip if not present
    pg_db = os.getenv("PG_DB")
    pg_user = os.getenv("PG_USER")
    pg_pass = os.getenv("PG_PASS")
    if not all([pg_db, pg_user, pg_pass]):
        pytest.skip("PG_DB/PG_USER/PG_PASS not set")

    with engine_swap(
        DB_ENGINE="postgres",
        DB_MODE="sync",
        DB_HOST=os.getenv("PG_HOST", "localhost"),
        DB_PORT=os.getenv("PG_PORT", "5432"),
        DB_USER=pg_user,
        DB_PASS=pg_pass,
        DB_NAME=pg_db,
    ):
        app = Application.get_app()
        app._providers.clear(); app._services.clear(); app._booted = False  # type: ignore
        app.register(SettingsProvider)
        app.register(DatabaseProvider)
        app.register(MigrationProvider)
        app.boot()

        eng = get_engine()
        assert _table_exists(eng), "migrations table missing on Postgres"
