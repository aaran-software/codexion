from cortex.database.schemas.builder import create, dropIfExists

def up():
    create("blog_category", lambda table: [
        table.id(),
        table.string("name"),
        table.timestamps()
    ])

def down():
    dropIfExists("blog_category")
