# tests/prefiq/database/test_mysql_like_schema.py
from __future__ import annotations
import socket
import pytest

from prefiq.database.schemas import blueprint as bp
from prefiq.database.schemas import builder as bld
from prefiq.database.schemas import queries as q


def _port_open(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except (ValueError, TypeError):
        return False


@pytest.mark.mariadb
def test_mysql_like_schema_crud(engine_swap, unique_table, mysql_cli):
    # Optional: skip if driver is missing
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
        pytest.skip(f"MySQL/MariaDB not reachable at {host}:{port}")

    # Use the CLI-provided database; override via --mysql-db if needed.
    with engine_swap(
        DB_ENGINE="mariadb",
        DB_MODE=mode,
        DB_HOST=str(host),
        DB_PORT=str(port),
        DB_USER=str(user),
        DB_PASS=str(password),
        DB_NAME=str(db),
    ):
        tname = unique_table

        def schema(t: bp.TableBlueprint):
            t.id()
            t.string("name", nullable=False)
            t.boolean("active", default=True)
            t.timestamps()
            t.index("idx_name", "name")
            t.unique("uq_name", ["name"])

        # Clean slates for idempotency
        bld.dropIfExists(tname)
        bld.create(tname, schema)

        q.insert(tname, {"name": "alice", "active": True})
        q.insert(tname, {"name": "bob", "active": False})

        row = q.select_one(tname, "name, active", "name = %s", ("alice",))
        assert row and str(row[0]).lower() == "alice"

        assert q.count(tname) == 2
        q.delete(tname, "name = %s", ("bob",))
        assert q.count(tname) == 1

        bld.dropIfExists(tname)
