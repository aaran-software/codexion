from cortex.database.schemas.builder import create, dropIfExists


DbTableIndex = 2

def up():
    create("users", lambda table: [
        table.id(),
        table.string("name"),
        table.string("email"),
        table.boolean("is_active"),
        table.timestamps()
    ])

def down():
    dropIfExists("users")
