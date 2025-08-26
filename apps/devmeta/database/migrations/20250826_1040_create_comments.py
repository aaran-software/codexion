# database/migrations/20250826_1040_create_comments.py

from prefiq.database.migrations.base import Migrations

class CreateComments(Migrations):
    APP_NAME    = "devmeta"
    TABLE_NAME  = "comments"
    ORDER_INDEX = 40

    def up(self) -> None:
        self.create(self.TABLE_NAME, lambda t: [
            t.id(),
            t.integer("task_id"),          # comment belongs to a task
            t.integer("author_id",nullable=True),
            t.string("author_name",nullable=True),
            t.text("body"),
            t.timestamps(),                # created_at = when commented; updated_at on edits
        ])

    def down(self) -> None:
        self.drop_if_exists(self.TABLE_NAME)
