from prefiq.database.schemas.builder import create, dropIfExists

# Keep the same table name your migrator expects; align with MIGR_TABLE/DEFAULT_TABLE_NAME
MIGRATIONS_TABLE = "devmeta_migrations"

def up():
    # Create the migrations bookkeeping table in DSL form
    create(MIGRATIONS_TABLE, lambda t: [
        t.id(),  # INTEGER PRIMARY KEY AUTOINCREMENT
        t.string("name", unique=True, nullable=False),
        t.integer("order_index", nullable=False),
        t.string("hash", nullable=False),
        t.timestamps(),
    ])

def down():
    dropIfExists(MIGRATIONS_TABLE)
