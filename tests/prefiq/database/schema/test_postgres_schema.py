# tests/prefiq/database/schema/test_postgres_schema.py
from __future__ import annotations
import pytest

from prefiq.database.schemas import blueprint as bp
from prefiq.database.schemas import builder as bld
from prefiq.database.schemas import queries as q


def _can_connect_pg(host: str, port: int, user: str, password: str, db: str) -> tuple[bool, str]:
    """
    Try a real psycopg connection (2s timeout). Return (ok, reason_if_not_ok).
    """
    try:
        import psycopg
    except Exception:
        return False, "psycopg driver not installed"

    try:
        conn = psycopg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=db,
            connect_timeout=2,  # seconds
            options="-c statement_timeout=2000",
        )
        conn.close()
        return True, ""
    except Exception as e:
        return False, f"cannot connect to Postgres at {host}:{port} db={db} user={user} · {e!s}"


@pytest.mark.postgres
def test_postgres_schema_crud(engine_swap, unique_table, pg_cli):
    host = str(pg_cli["host"])
    port = int(pg_cli["port"])
    user = str(pg_cli["user"])
    password = str(pg_cli["password"])
    db = str(pg_cli["db"])
    mode = pg_cli["mode"] if pg_cli["mode"] in ("sync", "async") else "sync"

    ok, why = _can_connect_pg(host, port, user, password, db)
    if not ok:
        pytest.skip(why)

    with engine_swap(
        DB_ENGINE="postgres",
        DB_MODE=mode,
        DB_HOST=host,
        DB_PORT=str(port),
        DB_USER=user,
        DB_PASS=password,
        DB_NAME=db,
    ):
        tname = unique_table

        def schema(t: bp.TableBlueprint):
            t.id()
            t.string("name", nullable=False)
            t.boolean("active", default=False)
            t.timestamps()
            t.index("idx_name", "name")
            t.unique("uq_name", ["name"])

        # Clean slate
        bld.dropIfExists(tname)
        bld.create(tname, schema)

        # %s placeholders get translated for Postgres ($1,$2,…) by the queries layer
        q.insert(tname, {"name": "alice", "active": True})
        q.update(tname, {"active": True}, "name = %s", ("alice",))

        row = q.select_one(tname, "name, active", "name = %s", ("alice",))
        assert row is not None and str(row[0]).lower() == "alice"

        assert q.count(tname) == 1
        q.delete(tname, "name = %s", ("alice",))
        assert q.count(tname) == 0

        bld.dropIfExists(tname)
