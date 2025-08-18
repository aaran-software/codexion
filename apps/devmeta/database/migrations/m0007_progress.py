from prefiq.database.schemas.builder import create, dropIfExists

TABLE = "progress"

def up():
    create(TABLE, lambda t: [
        t.id(),
        t.string("entity_type", nullable=False),
        t.integer("entity_id", nullable=False),
        t.integer("percent_done", default=0, nullable=False),
        t.datetime("updated_at", default="CURRENT_TIMESTAMP", nullable=False)
    ])

def down():
    dropIfExists(TABLE)
