# from __future__ import annotations
# from prefiq.database.schemas import blueprint as bp
# from prefiq.database.schemas import builder as bld
# from prefiq.database.schemas import queries as q
#
# def test_sqlite_schema_crud(engine_swap, unique_table, tmp_path):
#     db_file = tmp_path / "test.sqlite"
#     with engine_swap(DB_ENGINE="sqlite", DB_MODE="sync", DB_NAME=str(db_file)):
#         tname = unique_table
#
#         def schema(t: bp.TableBlueprint):
#             t.id()
#             t.string("name", nullable=False)
#             t.boolean("active", default=True)
#             t.timestamps()
#             t.index("idx_name", "name")  # will be created post-table
#
#         bld.dropIfExists(tname)
#         bld.create(tname, schema)
#
#         q.insert(tname, {"name": "alice", "active": True})
#         q.insert(tname, {"name": "bob", "active": False})
#
#         row = q.select_one(tname, "name, active", "name = ?", ("alice",))
#         assert row is not None and row[0] == "alice"
#
#         assert q.count(tname) == 2
#         q.delete(tname, "name = ?", ("bob",))
#         assert q.count(tname) == 1
#
#         bld.dropIfExists(tname)
