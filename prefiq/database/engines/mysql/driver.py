# prefiq/database/engines/mysql//driver.py

from prefiq.database.engines.mysql.sync_engine import SyncMysqlEngine
from prefiq.database.engines.mysql.async_engine import AsyncMysqlEngine
from prefiq.settings.get_settings import load_settings


class MariadbEngine:
    def __new__(cls):
        settings = load_settings()

        if not settings.DB_ENGINE:  # <-- IMPROVE: Add validation
            raise ValueError("DB_ENGINE must be set in settings")

        if settings.DB_MODE.lower() == "async":
            return AsyncMysqlEngine()
        return SyncMysqlEngine()
