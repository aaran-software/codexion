# prefiq/database/engines/postgres/driver.py

from __future__ import annotations
from prefiq.settings.get_settings import load_settings
from prefiq.database.engines.postgres.async_engine import AsyncPostgresEngine
from prefiq.database.engines.postgres.sync_engine import SyncPostgresEngine

class PostgresDBEngine:
    def __new__(cls):
        settings = load_settings()
        if not settings.DB_ENGINE:
            raise ValueError("DB_ENGINE must be set in settings")

        if settings.DB_MODE.lower() == "async":
            return AsyncPostgresEngine()
        return SyncPostgresEngine()
