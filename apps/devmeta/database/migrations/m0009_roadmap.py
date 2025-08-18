from prefiq.database.schemas.builder import create, dropIfExists

TABLE = "roadmap_milestones"

def up():
    create(TABLE, lambda t: [
        t.id(),
        t.integer("project_id", nullable=False),
        t.string("title", nullable=False),
        t.datetime("due_at", nullable=True),
        t.string("status", default="open", nullable=False),
        t.datetime("created_at", default="CURRENT_TIMESTAMP", nullable=False),
        t.datetime("updated_at", default="CURRENT_TIMESTAMP", nullable=False),
    ])

def down():
    dropIfExists(TABLE)
