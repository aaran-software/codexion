from __future__ import annotations
import os
import pytest

from prefiq.database.schemas import blueprint as bp
from prefiq.database.schemas import builder as bld
from prefiq.database.schemas import queries as q

pytestmark = pytest.mark.skipif(os.getenv("DB_TEST_MYSQL") != "1", reason="set DB_TEST_MYSQL=1 to run MySQL/MariaDB tests")

def test_mysql_like_schema_crud(engine_swap, unique_table):
    with engine_swap(DB_ENGINE="mariadb", DB_MODE="async"):
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
