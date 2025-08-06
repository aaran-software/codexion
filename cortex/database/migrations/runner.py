# =============================================================
# Migration Runner (runner.py)
#
# Applies all pending migrations for all apps.
# Tracks state in `migrations` table using schema builder.
# =============================================================

# cortex/database/migrations/runner.py

import datetime
from cortex.database.connection import db
from cortex.database.base_tables import migrations_table, tenant_table, users_table
from cortex.database.migrations.loader import (
    discover_all_app_migrations,
    resolve_and_load,
)
from cortex.database.schemas.queries import insert

# Core/system tables that should not be dropped
PROTECTED_TABLES = {"migrations, tenants, users"}


def _ensure_migrations_table():
    migrations_table.up()


def _is_applied(app: str, name: str, hash: str) -> bool:
    result = db.fetchone(
        "SELECT hash FROM migrations WHERE app = %s AND name = %s",
        (app, name)
    )
    if result:
        if result[0] != hash:
            print(f"⚠️  WARNING: {app}.{name} has changed since it was first applied.")
        return result[0] == hash
    return False


def _record_migration(app: str, name: str, index: int, hash: str):
    insert("migrations", {
        "app": app,
        "name": name,
        "order_index": index,
        "hash": hash,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow()
    })


def migrate_all():
    _ensure_migrations_table()

    apps = discover_all_app_migrations()

    for app, migration_list in apps.items():
        for i, name in enumerate(migration_list):
            try:
                mod, hash = resolve_and_load(app, name)

                if _is_applied(app, name, hash):
                    print(f"🟡 Skipping {app}.{name} (already applied)")
                    continue

                if not hasattr(mod, "up"):
                    raise AttributeError(f"Migration {name} in {app} has no `up()` function")

                print(f"✅ Running {app}.{name} ...")
                mod.up()
                _record_migration(app, name, i, hash)

            except Exception as e:
                print(f"❌ Failed to apply {app}.{name}: {e}")
                raise


def drop_all():
    tables = db.fetchall("SHOW TABLES")
    for (table_name,) in tables:
        if table_name in PROTECTED_TABLES:
            print(f"🛡️  Skipping protected table: {table_name}")
            continue
        print(f"🗑️  Dropping table: {table_name}")
        db.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
