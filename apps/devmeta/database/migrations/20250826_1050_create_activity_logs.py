# database/migrations/20250826_1050_create_activity_logs.py

from prefiq.database.migrations.base import Migrations

class CreateActivityLogs(Migrations):
    APP_NAME    = "devmeta"
    TABLE_NAME  = "activity_logs"
    ORDER_INDEX = 50

    def up(self) -> None:
        self.create(self.TABLE_NAME, lambda t: [
            t.id(),
            t.string("entity_type"),       # "project" | "task" | "comment" ...
            t.integer("entity_id"),        # id of the entity above
            t.string("action"),            # created / updated / status_changed / assigned / commented ...
            t.text("message",nullable=True),  # free-form description/diff
            t.integer("actor_id",nullable=True),
            t.string("actor_name",nullable=True),
            t.datetime("occurred_at",nullable=True),  # explicit event time (falls back to created_at)
            t.timestamps(),
        ])

    def down(self) -> None:
        self.drop_if_exists(self.TABLE_NAME)
