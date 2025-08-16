# cortex/database/engines/mariadb/driver.py

from cortex.database.engines.mariadb.sync_engine import SyncMariaDBEngine
from cortex.database.engines.mariadb.async_engine import AsyncMariaDBEngine
from cortex.core.settings import get_settings


class MongoDBEngine:
    def __new__(cls):
        settings = get_settings()

        if not settings.DB_ENGINE:  # <-- IMPROVE: Add validation
            raise ValueError("DB_ENGINE must be set in settings")

        if settings.DB_MODE.lower() == "async":
            return AsyncMariaDBEngine()
        return SyncMariaDBEngine()
