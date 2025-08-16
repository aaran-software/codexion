# cortex/core/providers/database_provider.py

from cortex.core.contracts.base_provider import BaseProvider

class DatabaseProvider(BaseProvider):
    def register(self):
        self.app.bind("database", {"engine": "sqlite", "url": "sqlite:///app.db"})

    def boot(self):
        print("[DatabaseProvider] Database initialized.")
