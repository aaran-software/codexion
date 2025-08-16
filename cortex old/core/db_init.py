# cortex/core/db_init.py

import pymysql
from pymysql.cursors import DictCursor
from cortex.core.settings import get_settings

def ensure_database_exists():
    settings = get_settings()

    if settings.DB_ENGINE.lower() != "mysql":
        return  # Only handle MySQL/MariaDB for now

    connection = None
    try:
        connection = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            cursorclass=DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES LIKE %s", (settings.DB_NAME,))
            result = cursor.fetchone()
            if result:
                print(f"[DB INIT] ✅ Database '{settings.DB_NAME}' already exists.")
            else:
                cursor.execute(f"CREATE DATABASE `{settings.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                print(f"[DB INIT] 🆕 Created database '{settings.DB_NAME}'.")
        connection.commit()
    except Exception as e:
        print(f"[DB INIT] ❌ Error connecting to database server: {e}")
    finally:
        if connection:
            connection.close()
