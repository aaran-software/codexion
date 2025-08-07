from cortex.database.schemas.builder import create, dropIfExists

def up():
    create("blog_posts", lambda table: [
        table.id(),
        table.string("title"),
        table.string("body"),
        table.timestamps()
    ])

def down():
    dropIfExists("blog_posts")
