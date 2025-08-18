# cortex/database/base_tables/000_migration_table.py

from prefiq.database.schemas.builder import create, dropIfExists

def up():
    create("tenants", lambda t: [
        t.id(),
        t.string("name"),
        t.timestamps()
    ])

def down():
    dropIfExists("tenants")
