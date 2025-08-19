from prefiq.database.engines.mariadb.sync_engine import SyncMariaDBEngine
from prefiq.database.engines.mariadb.async_engine import AsyncMariaDBEngine
from prefiq.settings.get_settings import load_settings


class PostgresDBEngine:
    def __new__(cls):
        settings = load_settings()

        if not settings.DB_ENGINE:  # <-- IMPROVE: Add validation
            raise ValueError("DB_ENGINE must be set in settings")

        if settings.DB_MODE.lower() == "async":
            return AsyncMariaDBEngine()
        return SyncMariaDBEngine()
