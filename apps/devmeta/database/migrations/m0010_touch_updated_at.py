# apps/devmeta/database/migrations/m0010_touch_updated_at.py
from prefiq.database.connection_manager import get_engine
from prefiq.database.dialects.registry import get_dialect

def up():
    d = get_dialect()
    if getattr(d, "name", "").lower() in ("sqlite",):
        return  # handled in app code or triggers if desired
    eng = get_engine()
    for table in ("todos", "notes", "projects", "assignees", "progress", "roadmap_milestones"):
        eng.execute(
            f"ALTER TABLE `{table}` "
            "MODIFY `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;"
        )

def down():
    d = get_dialect()
    if getattr(d, "name", "").lower() in ("sqlite",):
        return
    eng = get_engine()
    for table in ("todos", "notes", "projects", "assignees", "progress", "roadmap_milestones"):
        eng.execute(
            f"ALTER TABLE `{table}` "
            "MODIFY `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;"
        )
