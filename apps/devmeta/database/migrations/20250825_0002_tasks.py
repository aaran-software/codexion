from prefiq.database.migrations.base import Migrations

class Tasks(Migrations):
    APP_NAME    = "devmeta"
    TABLE_NAME  = "tasks"
    ORDER_INDEX = 2

    def up(self) -> None:
        self.create(self.TABLE_NAME, lambda t: [
            t.id(),
            t.bigint("project_id"),                    # FK → projects.id
            t.string("title"),
            t.text("description", nullable=True),
            t.string("assignee", nullable=True),
            t.string("status", default="todo"),        # todo|in_progress|blocked|done
            t.datetime("due_date", nullable=True),
            t.integer("priority", default=3),          # 1=high, 3=normal, 5=low
            t.timestamps(),
            t.index(["project_id", "status"]),
            # If your migration layer supports it, enable FK:
            # t.foreign("project_id").references("projects", "id").on_delete("CASCADE")
        ])

    def down(self) -> None:
        self.drop_if_exists(self.TABLE_NAME)
