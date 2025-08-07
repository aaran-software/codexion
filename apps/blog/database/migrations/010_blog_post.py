from cortex.database.schemas.builder import create, dropIfExists

def up():
    create("blog_post", lambda table: [
        table.id(),
        table.string("name"),
        table.timestamps()
    ])

def down():
    dropIfExists("blog_post")
