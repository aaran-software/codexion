# prefiq/database/engines/mongodb/sync_engine.py
from typing import Any, Optional
try:
    from pymongo import MongoClient
except (ValueError, TypeError):
    MongoClient = None

class SyncMongoEngine:
    """
    Not SQL. Exposes collection helpers for the builder’s Mongo path.
    """
    def __init__(self, settings) -> None:
        if MongoClient is None:
            raise RuntimeError("pymongo not installed. pip install pymongo")
        host = getattr(settings, "DB_HOST", "127.0.0.1")
        port = int(getattr(settings, "DB_PORT", 27017))
        user = getattr(settings, "DB_USER", None)
        password = getattr(settings, "DB_PASS", None)
        dbname = getattr(settings, "DB_NAME", "test")

        uri = f"mongodb://{host}:{port}"
        if user and password:
            uri = f"mongodb://{user}:{password}@{host}:{port}"
        self._client = MongoClient(uri)
        self._db = self._client[dbname]

    # This intentionally raises: SQL strings don’t apply to Mongo.
    def execute(self, sql: str, params: Optional[Any] = None) -> None:
        raise RuntimeError("MongoDB engine cannot execute SQL. Use collection helpers instead.")

    # Helpers the builder will call for Mongo
    def create_collection(self, name: str) -> None:
        if name not in self._db.list_collection_names():
            self._db.create_collection(name)

    def drop_collection(self, name: str) -> None:
        if name in self._db.list_collection_names():
            self._db.drop_collection(name)

    def close(self) -> None:
        self._client.close()

    @property
    def name(self) -> str:
        return "mongodb"
