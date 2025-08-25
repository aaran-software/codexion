# database/migrations/20250826_1030_create_task_assignees.py

from prefiq.database.migrations.base import Migrations

class CreateTaskAssignees(Migrations):
    APP_NAME    = "devmeta"
    TABLE_NAME  = "task_assignees"
    ORDER_INDEX = 30

    def up(self) -> None:
        self.create(self.TABLE_NAME, lambda t: [
            t.id(),
            t.integer("task_id"),          # FK to tasks.id (logical)
            t.integer("assignee_id",nullable=True),  # user id (if you have a users table)
            t.string("assignee_name",nullable=True), # fallback display name
            t.string("assignee_email",nullable=True),# fallback contact
            t.string("role",nullable=True),          # owner / contributor / reviewer
            t.datetime("assigned_at",nullable=True),
            t.timestamps(),
        ])

    def down(self) -> None:
        self.drop_if_exists(self.TABLE_NAME)
