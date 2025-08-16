# cortex/database/engines/mariadb/driver.py

from prefiq.database.engines.mariadb.sync_engine import SyncMariaDBEngine
from prefiq.database.engines.mariadb.async_engine import AsyncMariaDBEngine
from prefiq.core.settings import get_settings


class MariadbEngine:
    def __new__(cls):
        settings = get_settings()

        if not settings.DB_ENGINE:  # <-- IMPROVE: Add validation
            raise ValueError("DB_ENGINE must be set in settings")

        if settings.DB_MODE.lower() == "async":
            return AsyncMariaDBEngine()
        return SyncMariaDBEngine()
