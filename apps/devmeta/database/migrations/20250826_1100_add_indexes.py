from prefiq.database.migrations.base import Migrations

class AddIndexes(Migrations):
    APP_NAME    = "devmeta"
    TABLE_NAME  = "_meta"     # not used; just for display
    ORDER_INDEX = 60

    def up(self) -> None:
        from prefiq.database.schemas.builder import createIndex
        createIndex("tasks", "idx_tasks_project", ["project_id"])
        createIndex("task_assignees", "idx_ta_task", ["task_id"])
        createIndex("comments", "idx_comments_task", ["task_id"])
        createIndex("activity_logs", "idx_logs_entity", ["entity_type", "entity_id"])
        createIndex("projects", "idx_projects_status", ["status"])

    def down(self) -> None:
        # optional: drop indexes if your builder has dropIndex; otherwise leave as-is
        pass
