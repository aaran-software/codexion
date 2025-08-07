from cortex.database.schemas.builder import create, dropIfExists

def up():
    create("dashboard", lambda table: [
        table.id(),
        table.string("name"),
        table.timestamps()
    ])

def down():
    dropIfExists("dashboard")
