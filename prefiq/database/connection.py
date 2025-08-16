# prefiq/database/connection.py

from prefiq.core.settings import get_settings

def _resolve_db_engine():
    settings = get_settings()
    db_engine = settings.DB_ENGINE.lower()

    if db_engine == "mariadb":
        from prefiq.database.engines.mariadb.driver import MariadbEngine
        return MariadbEngine()

    elif db_engine == "mysql":
        from prefiq.database.engines.mysql.driver import MySQLDBEngine
        return MySQLDBEngine()

    elif db_engine == "postgres":
        from prefiq.database.engines.postgres.driver import PostgresDBEngine
        return PostgresDBEngine()

    elif db_engine == "sqlite":
        from prefiq.database.engines.sqlite.driver import SQLiteDBEngine
        return SQLiteDBEngine()

    elif db_engine == "mongodb":
        from prefiq.database.engines.mongo.driver import MongoDBEngine
        return MongoDBEngine()

    else:
        raise ValueError(f"Unsupported DB_ENGINE: {db_engine}")


# Global db instance resolved only once
db = _resolve_db_engine()
