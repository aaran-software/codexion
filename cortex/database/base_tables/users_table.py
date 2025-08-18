# cortex/database/base_tables/000_migration_table.py

from prefiq.database.schemas.builder import create, drop_if_exists

def up():
    create("users", lambda t: [
        t.id(),
        t.string("name"),
        t.string("email"),
        t.boolean("is_active"),
        t.timestamps()
    ])

def down():
    drop_if_exists("users")
