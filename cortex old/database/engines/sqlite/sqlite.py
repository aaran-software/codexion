# cortex/db/drivers/sqlite.py

import sqlite3
from cortex.core.settings import get_settings
from cortex.database.base_engine import BaseDBEngine

class SQLiteDBEngine(BaseDBEngine):
    def __init__(self):
        self.settings = get_settings()
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.settings.DB_NAME)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def test_connection(self) -> bool:
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"❌ SQLite connection failed: {e}")
            return False
