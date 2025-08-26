# apps/devmeta/database/seeders/seed_dev.py
from __future__ import annotations
import os
from pathlib import Path
import sqlite3

DB_FILE = Path(r"E:\Workspace\codexion\database\devmeta.sqlite")  # <- this is the file your peek showed
os.environ.setdefault("DB_ENGINE", "sqlite")
os.environ.setdefault("DB_MODE", "sync")
os.environ["DB_NAME"] = str(DB_FILE)  # keep env in sync so other tools see the same file

def row_exists(cur, sql: str, params=()):
    cur.execute(sql, params)
    return cur.fetchone() is not None

def main():
    print("DB:", DB_FILE)
    con = sqlite3.connect(DB_FILE)
    try:
        cur = con.cursor()

        # Sanity: bail out if tables are missing
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1")
        names = {r[0] for r in cur.fetchall()}
        required = {"projects", "tasks", "task_assignees", "comments", "activity_logs"}
        missing = sorted(required - names)
        if missing:
            raise SystemExit(f"❌ Missing tables: {', '.join(missing)}. Run migrations against this DB first.")

        # Ensure project
        if not row_exists(cur, "SELECT 1 FROM projects WHERE code=?", ("PRJ-001",)):
            cur.execute(
                "INSERT INTO projects (code, name, description, status, start_at, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                ("PRJ-001", "Prefiq Devmeta", "Demo project", "active"),
            )

        # Get project id
        cur.execute("SELECT id FROM projects WHERE code=?", ("PRJ-001",))
        proj_id = cur.fetchone()[0]

        # Ensure task
        if not row_exists(cur, "SELECT 1 FROM tasks WHERE project_id=? AND title=?", (proj_id, "Wire migrations")):
            cur.execute(
                "INSERT INTO tasks (project_id, title, description, status, priority, due_at, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, DATE('now','+7 day'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                (proj_id, "Wire migrations", "Create core tables", "todo", 2),
            )

        cur.execute("SELECT id FROM tasks WHERE project_id=? AND title=?", (proj_id, "Wire migrations"))
        task_id = cur.fetchone()[0]

        # Ensure assignee
        if not row_exists(cur, "SELECT 1 FROM task_assignees WHERE task_id=? AND assignee_id=?", (task_id, 101)):
            cur.execute(
                "INSERT INTO task_assignees (task_id, assignee_id, role, created_at, updated_at) "
                "VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                (task_id, 101, "owner"),
            )

        # Ensure comment
        if not row_exists(cur, "SELECT 1 FROM comments WHERE task_id=? AND body=?", (task_id, "Initial setup comment")):
            cur.execute(
                "INSERT INTO comments (task_id, author_id, body, created_at, updated_at) "
                "VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                (task_id, 101, "Initial setup comment"),
            )

        # Ensure activity
        if not row_exists(cur, "SELECT 1 FROM activity_logs WHERE entity_type='task' AND entity_id=? AND action='created'", (task_id,)):
            cur.execute(
                "INSERT INTO activity_logs (entity_type, entity_id, action, message, actor_id, occurred_at, created_at, updated_at) "
                "VALUES ('task', ?, 'created', ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                (task_id, "seed:init", 101),
            )

        con.commit()
        print("✅ Seed committed.")
        # Show counts
        for t in ["projects", "tasks", "task_assignees", "comments", "activity_logs"]:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            print(f"{t}: {cur.fetchone()[0]}")
    finally:
        con.close()

if __name__ == "__main__":
    main()
