# tests/prefiq/database/test_mysql_like_schema.py
from __future__ import annotations
import os, socket
import pytest

from prefiq.settings.get_settings import load_settings
from prefiq.database.schemas import blueprint as bp
from prefiq.database.schemas import builder as bld
from prefiq.database.schemas import queries as q

def _truthy(x: str) -> bool:
    return x.strip().lower() in ("1", "true", "yes", "y", "on")

def _from_settings_bool(name: str, default: bool = False) -> bool:
    try:
        s = load_settings()
        v = getattr(s, name, default)
        return _truthy(v) if isinstance(v, str) else bool(v)
    except Exception:
        return default

def _port_open(host: str, port: int, timeout: float = 0.3) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def _mysql_enabled_and_ready() -> tuple[bool, str]:
    enabled = (_truthy(os.getenv("DB_TEST_MYSQL", "")) or _from_settings_bool("DB_TEST_MYSQL", False))
    if not enabled:
        return False, "Enable with DB_TEST_MYSQL=1 (env or settings)"
    # quick reachability probe
    s = load_settings()
    host = os.getenv("DB_HOST", getattr(s, "DB_HOST", "127.0.0.1"))
    port = int(os.getenv("DB_PORT", getattr(s, "DB_PORT", 3306)))
    if not _port_open(host, port):
        return False, f"MySQL/MariaDB not reachable at {host}:{port}"
    return True, ""

_ok, _why = _mysql_enabled_and_ready()
pytestmark = pytest.mark.skipif(not _ok, reason=_why or "MySQL disabled")

def test_mysql_like_schema_crud(engine_swap, unique_table):
    # Use a safe default DB name; override with DB_NAME_MYSQL if you want a specific schema
    with engine_swap(
        DB_ENGINE="mariadb",
        DB_MODE="async",
        DB_HOST=os.getenv("DB_HOST", "127.0.0.1"),
        DB_PORT=os.getenv("DB_PORT", "3306"),
        DB_USER=os.getenv("DB_USER", "root"),
        DB_PASS=os.getenv("DB_PASS", "Computer.1"),
        DB_NAME=os.getenv("DB_NAME_MYSQL", "mysql"),  # <— was ":memory:" via session defaults
    ):
        tname = unique_table

        def schema(t: bp.TableBlueprint):
            t.id()
            t.string("name", nullable=False)
            t.boolean("active", default=True)
            t.timestamps()
            t.index("idx_name", "name")
            t.unique("uq_name", ["name"])

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
