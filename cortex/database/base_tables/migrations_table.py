# cortex/database/base_tables/000_migration_table.py

from cortex.database.schemas.builder import create, dropIfExists

def up():
    create("migrations", lambda t: [
        t.id(),
        t.string("app"),
        t.string("name"),
        t.integer("order_index"),
        t.string("hash"),
        t.timestamps()
    ])

def down():
    dropIfExists("migrations")
