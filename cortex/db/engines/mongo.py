# cortex/db/drivers/mongo.py

from pymongo import MongoClient
from cortex.core.settings import get_settings
from cortex.db.base_engine import BaseDBEngine

class MongoDBEngine(BaseDBEngine):
    def __init__(self):
        self.settings = get_settings()
        self.client = None

    def connect(self):
        if self.client is None:
            uri = f"mongodb://{self.settings.DB_USER}:{self.settings.DB_PASS}@{self.settings.DB_HOST}:{self.settings.DB_PORT}/{self.settings.DB_NAME}"
            self.client = MongoClient(uri)
        return self.client[self.settings.DB_NAME]

    def test_connection(self) -> bool:
        try:
            db = self.connect()
            # list collections to test
            _ = db.list_collection_names()
            return True
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            return False
