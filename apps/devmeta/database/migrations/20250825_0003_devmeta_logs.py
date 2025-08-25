from prefiq.database.migrations.base import Migrations

class DevmetaLogs(Migrations):
    APP_NAME    = "devmeta"
    TABLE_NAME  = "devmeta_logs"
    ORDER_INDEX = 3

    def up(self) -> None:
        self.create(self.TABLE_NAME, lambda t: [
            t.id(),
            t.bigint("project_id", nullable=True),     # optional FK
            t.bigint("task_id", nullable=True),        # optional FK
            t.string("action"),                        # e.g., 'task.created', 'status.changed'
            t.string("actor", nullable=True),          # user/email/service
            t.text("meta", nullable=True),             # JSON/text payload
            t.datetime("created_at"),                  # when it happened
            t.index(["project_id"]),
            t.index(["task_id"]),
        ])

    def down(self) -> None:
        self.drop_if_exists(self.TABLE_NAME)
