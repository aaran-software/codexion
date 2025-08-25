# database/migrations/20250826_1010_create_projects.py

from prefiq.database.migrations.base import Migrations

class CreateProjects(Migrations):
    APP_NAME    = "devmeta"
    TABLE_NAME  = "projects"
    ORDER_INDEX = 10

    def up(self) -> None:
        self.create(self.TABLE_NAME, lambda t: [
            t.id(),
            t.string("code"),              # optional short code like "PRJ-001"
            t.string("name"),
            t.text("description",nullable=True),
            t.string("status"),            # planned / active / on_hold / done / cancelled
            t.datetime("start_at",nullable=True),
            t.datetime("end_at",nullable=True),
            t.timestamps(),                # created_at, updated_at
        ])

    def down(self) -> None:
        self.drop_if_exists(self.TABLE_NAME)
