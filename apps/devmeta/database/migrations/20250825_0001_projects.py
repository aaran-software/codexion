from prefiq.database.migrations.base import Migrations

class Projects(Migrations):
    APP_NAME    = "devmeta"
    TABLE_NAME  = "projects"
    ORDER_INDEX = 1

    def up(self) -> None:
        self.create(self.TABLE_NAME, lambda t: [
            t.id(),                              # id BIGINT PK / INTEGER PK under sqlite
            t.string("name", unique=True),
            t.text("description", nullable=True),
            t.string("repo_url", nullable=True),
            t.string("owner", nullable=True),
            t.string("status", default="active"),   # active|paused|archived
            t.timestamps(),                         # created_at, updated_at
        ])

    def down(self) -> None:
        self.drop_if_exists(self.TABLE_NAME)
