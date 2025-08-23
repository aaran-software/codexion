from __future__ import annotations
import os
import pytest

from prefiq.database.schemas import blueprint as bp
from prefiq.database.schemas import builder as bld
from prefiq.database.schemas import queries as q

pytestmark = pytest.mark.skipif(os.getenv("DB_TEST_PG") != "1", reason="set DB_TEST_PG=1 to run Postgres tests")

def test_postgres_schema_crud(engine_swap, unique_table):
    with engine_swap(DB_ENGINE="postgres", DB_MODE="async", DB_HOST=os.getenv("DB_HOST","127.0.0.1")):
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
