from prefiq.database.schemas.builder import create, drop_if_exists

TABLE = "logs"

def up():
    create(TABLE, lambda t: [
        t.id(),
        t.string("level", default="info", nullable=False),
        t.string("message", nullable=False),
        t.text("details", nullable=True),
        t.text("context", nullable=True),
        t.string("user", nullable=True),
        t.datetime("created_at", default="CURRENT_TIMESTAMP", nullable=False),
    ])

def down():
    drop_if_exists(TABLE)
