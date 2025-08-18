from prefiq.database.schemas.builder import create, drop_if_exists

TABLE = "assignees"

def up():
    create(TABLE, lambda t: [
        t.id(),
        t.string("handle", nullable=False),
        t.string("name", nullable=False),
        t.string("email", nullable=True),
        t.string("role", nullable=True),
        t.datetime("created_at", default="CURRENT_TIMESTAMP", nullable=False),
        t.datetime("updated_at", default="CURRENT_TIMESTAMP", nullable=False),
    ])

def down():
    drop_if_exists(TABLE)
