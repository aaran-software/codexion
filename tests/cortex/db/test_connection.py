import pytest

from cortex.db.engines.mysql import MySQLDBEngine
from cortex.db.engines.mariadb import MariaDBEngine
from cortex.db.engines.postgres import PostgresDBEngine
from cortex.db.engines.sqlite import SQLiteDBEngine
from cortex.db.engines.mongo import MongoDBEngine

# def test_mysql_connection():
#     engine = MySQLDBEngine()
#     assert engine.test_connection() == True, "MySQL connection failed"

def test_mariadb_connection():
    engine = MariaDBEngine()
    assert engine.test_connection() == True, "MariaDB connection failed"

# def test_postgres_connection():
#     engine = PostgresDBEngine()
#     assert engine.test_connection() == True, "PostgreSQL connection failed"

def test_sqlite_connection(tmp_path):
    # Example: SQLite test DB in temp directory
    from cortex.core.settings import clear_settings_cache, Settings

    db_path = tmp_path / "test.sqlite3"
    settings = Settings(DB_ENGINE="sqlite", DB_NAME=str(db_path), TESTING=True)
    clear_settings_cache()

    engine = SQLiteDBEngine()
    assert engine.test_connection() == True, "SQLite connection failed"

# def test_mongo_connection():
#     engine = MongoDBEngine()
#     assert engine.test_connection() == True, "MongoDB connection failed"
