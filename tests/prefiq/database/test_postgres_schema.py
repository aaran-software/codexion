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

def _pg_enabled_and_ready() -> tuple[bool, str]:
    # enabled via env or settings
    enabled = (_truthy(os.getenv("DB_TEST_PG", "")) or _from_settings_bool("DB_TEST_PG", False))
    if not enabled:
        return False, "Enable with DB_TEST_PG=1 (env or settings)"
    # quick reachability probe
    s = load_settings()
    host = os.getenv("DB_HOST", getattr(s, "DB_HOST", "127.0.0.1"))
    port = int(os.getenv("DB_PORT", getattr(s, "DB_PORT", 5432)))
    if not _port_open(host, port):
        return False, f"Postgres not reachable at {host}:{port}"
    return True, ""

_ok, _why = _pg_enabled_and_ready()
pytestmark = pytest.mark.skipif(not _ok, reason=_why or "PG disabled")

def test_postgres_schema_crud(engine_swap, unique_table):
    # Use a safe default DB; override via DB_NAME_PG if you want (e.g., prefiq_dev)
    with engine_swap(
        DB_ENGINE="postgres",
        DB_MODE="async",
        DB_HOST=os.getenv("DB_HOST", "127.0.0.1"),
        DB_PORT=os.getenv("DB_PORT", "5432"),
        DB_USER=os.getenv("DB_USER", "postgres"),
        DB_PASS=os.getenv("DB_PASS", "DbPass1@@"),
        DB_NAME=os.getenv("DB_NAME_PG", "postgres"),
    ):
        tname = unique_table

        def schema(t: bp.TableBlueprint):
            t.id()
            t.string("name", nullable=False)
            t.boolean("active", default=False)
            t.timestamps()
            t.index("idx_name", "name")
            t.unique("uq_name", ["name"])

        bld.dropIfExists(tname)
        bld.create(tname, schema)

        q.insert(tname, {"name": "alice", "active": True})
        q.update(tname, {"active": True}, 'name = %s', ("alice",))

        row = q.select_one(tname, "name, active", 'name = %s', ("alice",))
        assert row is not None and str(row[0]).lower() == "alice"

        assert q.count(tname) == 1
        q.delete(tname, 'name = %s', ("alice",))
        assert q.count(tname) == 0

        bld.dropIfExists(tname)

