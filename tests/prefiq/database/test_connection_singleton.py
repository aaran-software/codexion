# # tests/prefiq/database/test_connection_singleton.py
# from __future__ import annotations
# from prefiq.database.connection import get_engine, reset_engine, reload_engine_from_env
# from prefiq.settings.get_settings import clear_settings_cache
# import os
#
# def test_connection_singleton_rebuilds_on_reset(tmp_path):
#     # point SQLite at a file so we don't rely on :memory:
#     db_file = tmp_path / "unit.sqlite"
#     os.environ["DB_ENGINE"] = "sqlite"
#     os.environ["DB_MODE"] = "sync"
#     os.environ["DB_NAME"] = str(db_file)
#
#     clear_settings_cache()
#     reset_engine()
#     eng1 = reload_engine_from_env()
#
#     # Should return the same instance without changes
#     eng2 = get_engine()
#     assert eng1 is eng2
#
#     # Reset must drop the singleton; next call should create a new instance
#     reset_engine()
#     eng3 = get_engine()
#     assert eng3 is not eng2
