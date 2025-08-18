from prefiq.database.schemas.builder import create, dropIfExists

TABLE = "projects"

def up():
    create(TABLE, lambda t: [
        t.id(),
        t.string("key", nullable=False),
        t.string("name", nullable=False),
        t.text("description", nullable=True),
        t.string("status", default="open", nullable=False),
        t.datetime("created_at", default="CURRENT_TIMESTAMP", nullable=False),
        t.datetime("updated_at", default="CURRENT_TIMESTAMP", nullable=False)
    ])

def down():
    dropIfExists(TABLE)
