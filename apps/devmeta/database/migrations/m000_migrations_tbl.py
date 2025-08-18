from prefiq.database.schemas.builder import create, drop_if_exists

TABLE = "devmeta_migrations"

def up():
    create(TABLE, lambda t: [
        t.id(),
        t.string("name", unique=True, nullable=False),
        t.integer("order_index", nullable=False),
        t.string("hash", nullable=False),
        t.datetime("applied_at", default="CURRENT_TIMESTAMP", nullable=False),
    ])

def down():
    drop_if_exists(TABLE)
