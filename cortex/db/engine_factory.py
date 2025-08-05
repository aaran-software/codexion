from cortex.core.settings import get_settings


def get_db_engine():
    settings = get_settings()
    db_engine = settings.DB_ENGINE.lower()

    if db_engine == "mariadb":
        from cortex.db.engines.mariadb import MariaDBEngine
        return MariaDBEngine()

    elif db_engine == "mysql":
        from cortex.db.engines.mysql import MySQLDBEngine
        return MySQLDBEngine()

    elif db_engine == "postgres":
        from cortex.db.engines.postgres import PostgresDBEngine
        return PostgresDBEngine()

    elif db_engine == "sqlite":
        from cortex.db.engines.sqlite import SQLiteDBEngine
        return SQLiteDBEngine()

    elif db_engine == "mongodb":
        from cortex.db.engines.mongo import MongoDBEngine
        return MongoDBEngine()

    else:
        raise ValueError(f"Unsupported DB_ENGINE: {db_engine}")
