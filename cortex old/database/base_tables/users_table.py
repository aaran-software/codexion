# cortex/database/base_tables/000_migration_table.py

from cortex.database.schemas.builder import create, dropIfExists

def up():
    create("users", lambda t: [
        t.id(),
        t.string("name"),
        t.string("email"),
        t.boolean("is_active"),
        t.timestamps()
    ])

def down():
    dropIfExists("users")
