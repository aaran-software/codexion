from prefiq.database.schemas.builder import create, dropIfExists

TABLE = "notes"

def up():
    create(TABLE, lambda t: [
        t.id(),
        t.string("title", nullable=False),
        t.text("content", nullable=False),
        t.text("tags", nullable=True),
        t.integer("linked_todo_id", nullable=True),
        t.times("created_at", default="CURRENT_TIMESTAMP", nullable=False),
        t.datetime("updated_at", default="CURRENT_TIMESTAMP", nullable=False)
    ])

def down():
    dropIfExists(TABLE)
