from prefiq.database.schemas.builder import create, dropIfExists

TABLE = "reviews"

def up():
    create(TABLE, lambda t: [
        t.id(),
        t.string("entity_type", nullable=False),
        t.integer("entity_id", nullable=False),
        t.text("comments", nullable=True),
        t.integer("rating", nullable=True),
        t.datetime("created_at", default="CURRENT_TIMESTAMP", nullable=False),
    ])

def down():
    dropIfExists(TABLE)
