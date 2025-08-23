# cortex/database/base_tables/m000_migration_table.py

from prefiq.database.schemas.builder import create, drop_if_exists

def migrations_table_up():
    create("migrations", lambda t: [
        t.id(),
        t.string("app"),
        t.string("name"),
        t.integer("order_index"),
        t.string("hash"),
        t.timestamps()
    ])

def migrations_table_down():
    drop_if_exists("migrations")
