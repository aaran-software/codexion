from cortex.database.schemas.builder import create, dropIfExists

def up():
    create("blog_reply", lambda table: [
        table.id(),
        table.string("name"),
    ])

def down():
    dropIfExists("blog_reply")
