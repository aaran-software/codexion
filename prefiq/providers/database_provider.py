# prefiq/core/providers/database_provider.py

from prefiq.core.contracts.base_provider import BaseProvider, register_provider
from prefiq.database.connection import db  # global engine resolver

@register_provider
class DatabaseProvider(BaseProvider):
    """
    Database Provider
    -----------------
    Wraps the engine resolver into the Application container.
    Makes `db` globally available via app.resolve("db").
    """

    def __init__(self, app):
        super().__init__(app)
        self.engine = db   # resolved engine instance

    def register(self) -> None:
        # Bind engine into the app
        self.app.bind("db", self.engine)

    def boot(self) -> None:
        # Test connection during boot
        try:
            if self.engine.test_connection():
                print("[DatabaseProvider] Connected successfully.")
            else:
                print("[DatabaseProvider] Connection failed.")
        except Exception as e:
            print(f"[DatabaseProvider] Error testing connection: {e}")
