from prefiq.database.schemas.builder import create, dropIfExists

def up():
    create("todos", lambda t: [
        t.id(),
        t.string("title"),
        t.string("status", default="open"),
        t.integer("priority", default=3),
        t.string("project", nullable=True),
        t.datetime("due_at", nullable=True),
        t.timestamps(),
        t.datetime("completed_at", nullable=True),
    ])

def down():
    dropIfExists("todos")
