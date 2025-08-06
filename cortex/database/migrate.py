import os
import importlib.util
import glob

from cortex.core.settings import get_settings
from cortex.db import get_db_engine


def get_applied_migrations(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("SELECT name FROM schema_migrations")
    return set(row["name"] for row in cursor.fetchall())


def mark_migration_applied(cursor, name):
    cursor.execute("INSERT INTO schema_migrations (name) VALUES (%s)", (name,))


def run_migrations():
    settings = get_settings()
    engine = get_db_engine()
    conn = engine.connect()
    cursor = conn.cursor()

    print("🔍 Checking for unapplied migrations...")

    migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
    migration_files = sorted(glob.glob(os.path.join(migrations_dir, "*.py")))
    applied = get_applied_migrations(cursor)

    for path in migration_files:
        name = os.path.basename(path)

        if name in applied or name == "__init__.py":
            continue

        print(f"⚙️  Applying migration: {name}")

        # Load and run the migration's `up()` function
        spec = importlib.util.spec_from_file_location("migration", path)
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)

        migration.up(cursor)
        mark_migration_applied(cursor, name)

    conn.commit()
    cursor.close()
    print("✅ All migrations applied.")

