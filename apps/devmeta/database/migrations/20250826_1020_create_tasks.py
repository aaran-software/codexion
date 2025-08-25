# database/migrations/20250826_1020_create_tasks.py

from prefiq.database.migrations.base import Migrations

class CreateTasks(Migrations):
    APP_NAME    = "devmeta"
    TABLE_NAME  = "tasks"
    ORDER_INDEX = 20

    def up(self) -> None:
        self.create(self.TABLE_NAME, lambda t: [
            t.id(),
            t.integer("project_id"),       # FK to projects.id (logical)
            t.string("title"),
            t.text("description",nullable=True),
            t.string("status"),            # todo / in_progress / review / done
            t.integer("priority",nullable=True),  # 1..5 or similar
            t.datetime("due_at",nullable=True),
            t.timestamps(),
        ])

    def down(self) -> None:
        self.drop_if_exists(self.TABLE_NAME)
