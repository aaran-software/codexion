# cortex/db/drivers/postgres.py

import psycopg2
from psycopg2.extras import RealDictCursor
from cortex.core.settings import get_settings
from cortex.db import BaseDBEngine

class PostgresDBEngine(BaseDBEngine):
    def __init__(self):
        self.settings = get_settings()
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                host=self.settings.DB_HOST,
                user=self.settings.DB_USER,
                password=self.settings.DB_PASS,
                dbname=self.settings.DB_NAME,
                port=self.settings.DB_PORT,
                cursor_factory=RealDictCursor
            )
        return self.conn

    def test_connection(self) -> bool:
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
            return False
