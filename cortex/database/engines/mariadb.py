# cortex/database/engines/mariadb.py

import mariadb
from cortex.core.settings import get_settings
from cortex.database.base_engine import BaseDBEngine

class MariaDBEngine(BaseDBEngine):
    def __init__(self):
        self.settings = get_settings()
        self.conn = None
        self._cursor = None

    def connect(self):
        if self.conn is None:
            self.conn = mariadb.connect(
                host=self.settings.DB_HOST,
                user=self.settings.DB_USER,
                password=self.settings.DB_PASS,
                database=self.settings.DB_NAME,
                port=self.settings.DB_PORT
            )
            self._cursor = self.conn.cursor()
        return self.conn

    def cursor(self):
        if self._cursor is None:
            self.connect()
        return self._cursor

    def execute(self, sql: str, params=None):
        cur = self.cursor()
        cur.execute(sql, params or ())
        self.conn.commit()

    def fetchone(self, sql: str, params=None):
        cur = self.cursor()
        cur.execute(sql, params or ())
        return cur.fetchone()

    def test_connection(self) -> bool:
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"❌ MariaDB connection failed: {e}")
            return False
