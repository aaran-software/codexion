from prefiq.database.connection_manager import get_engine
from prefiq.database.dialects.registry import get_dialect

TABLES = ("todos", "notes", "projects", "assignees", "progress", "roadmap_milestones")

def _dialect_name_lower() -> str:
    d = get_dialect()
    n = getattr(d, "name", None)
    if callable(n):
        try:
            n = n()
        except Exception:
            n = None
    return (n if isinstance(n, str) else type(d).__name__).lower()

def up():
    dname = _dialect_name_lower()
    if dname in ("sqlite",):
        # Skip: use app-side touch/trigger for SQLite if desired
        return
    eng = get_engine()
    for table in TABLES:
        eng.execute(
            f"ALTER TABLE `{table}` "
            "MODIFY `updated_at` DATETIME NOT NULL "
            "DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;"
        )

def down():
    dname = _dialect_name_lower()
    if dname in ("sqlite",):
        return
    eng = get_engine()
    for table in TABLES:
        eng.execute(
            f"ALTER TABLE `{table}` "
            "MODIFY `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;"
        )
