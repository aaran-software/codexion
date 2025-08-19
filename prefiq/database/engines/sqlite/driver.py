# =============================================================
# SQLite Engine Driver (driver.py)
# file path: prefiq/database/engines/sqlite/driver.py
#
# Author: Sundar
# Created: 2025-08-18
#
# Purpose:
#   - Factory-style entrypoint for instantiating SQLite engine.
#   - Returns either Sync or Async engine depending on DB_MODE.
#
# Notes for Developers:
#   - Reads DB_ENGINE and DB_MODE from global settings.
#   - Raises ValueError if DB_ENGINE is misconfigured.
#   - Keeps the API consistent with MariadbEngine.
# =============================================================

from prefiq.database.engines.sqlite.sync_engine import SQLiteEngine
from prefiq.database.engines.sqlite.async_engine import AsyncSQLiteEngine
from prefiq.settings.get_settings import load_settings


class SQLiteEngine:
    def __new__(cls):
        settings = load_settings()

        if not settings.DB_ENGINE:
            raise ValueError("DB_ENGINE must be set in settings")

        if settings.DB_ENGINE.lower() != "sqlite":
            raise ValueError(
                f"SQLiteEngine can only be used when DB_ENGINE='sqlite', "
                f"got: {settings.DB_ENGINE!r}"
            )

        if settings.DB_MODE and settings.DB_MODE.lower() == "async":
            return AsyncSQLiteEngine()

        return SQLiteEngine()
