import mariadb

from cortex.core.settings import get_settings
from cortex.db.base_engine import BaseDBEngine

class MariaDBEngine(BaseDBEngine):
    def __init__(self):
        self.settings = get_settings()
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = mariadb.connect(
                host=self.settings.DB_HOST,
                user=self.settings.DB_USER,
                password=self.settings.DB_PASS,
                database=self.settings.DB_NAME,
                port=self.settings.DB_PORT
            )
        return self.conn

    def test_connection(self) -> bool:
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"❌ MariaDB connection failed: {e}")
            return False
