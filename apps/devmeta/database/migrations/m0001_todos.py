from prefiq.database.schemas.builder import create, dropIfExists

def up(conn=None):
    create("todos", lambda t: [
        t.id(),
        t.string("title", nullable=False),
        t.string("status", default="open", nullable=False),
        t.integer("priority", default=3, nullable=False),
        t.string("project", nullable=True),
        t.datetime("due_at", nullable=True),
        t.datetime("created_at", default="CURRENT_TIMESTAMP", nullable=False),
        t.datetime("updated_at", default="CURRENT_TIMESTAMP", nullable=False),
        t.datetime("completed_at", nullable=True),
    ])

def down(conn=None):
    dropIfExists("todos")
