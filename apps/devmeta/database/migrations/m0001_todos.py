from prefiq.database.schemas.builder import create, drop_if_exists

TABLE = "todos"

def up():
    create(TABLE, lambda t: [
        t.id(),
        t.string("title", nullable=False),
        t.string("status", default="open", nullable=False),
        t.integer("priority", default=3, nullable=False),
        t.string("project", nullable=True),
        t.datetime("due_at", nullable=True),
        t.datetime("created_at", default="CURRENT_TIMESTAMP", nullable=False),
        t.datetime("updated_at", default="CURRENT_TIMESTAMP", nullable=False),
        t.datetime("completed_at", nullable=True),
        t.string("tags", nullable=True),
    ])

def down():
    drop_if_exists(TABLE)
