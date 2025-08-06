# cortex/database/connection.py

from cortex.core.settings import get_settings

def _resolve_db_engine():
    settings = get_settings()
    db_engine = settings.DB_ENGINE.lower()

    if db_engine == "mariadb":
        from cortex.database.engines.mariadb.driver import MariadbEngine
        return MariadbEngine()

    elif db_engine == "mysql":
        from cortex.database.engines.mysql.driver import MySQLDBEngine
        return MySQLDBEngine()

    elif db_engine == "postgres":
        from cortex.database.engines.postgres.driver import PostgresDBEngine
        return PostgresDBEngine()

    elif db_engine == "sqlite":
        from cortex.database.engines.sqlite.driver import SQLiteDBEngine
        return SQLiteDBEngine()

    elif db_engine == "mongodb":
        from cortex.database.engines.mongo.driver import MongoDBEngine
        return MongoDBEngine()

    else:
        raise ValueError(f"Unsupported DB_ENGINE: {db_engine}")


# Global db instance resolved only once
db = _resolve_db_engine()
