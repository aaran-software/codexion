# providers/database_provider.py

from cortex.services import ServiceProvider
from cortex.core.settings import get_settings
from cortex.container import container
from cortex.db import get_db_engine

class DatabaseServiceProvider(ServiceProvider):
    def register(self):
        settings = get_settings()

        # Dynamically get DB engine (MySQL, PostgreSQL, etc.)
        engine = get_db_engine()

        # Bind engine and settings to the container
        container.instance("db_engine", engine)
        container.instance("settings", settings)

    def boot(self):
        engine = container.resolve("db_engine")
        if engine.test_connection():
            print("✅ Database connection established.")
        else:
            print("❌ Database connection failed.")
