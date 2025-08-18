from __future__ import annotations

from datetime import datetime, UTC
from typing import Any, Callable, Optional, List

from prefiq.log.logger import get_logger

LOG = get_logger("prefiq.devmeta.service.todo")

# connect_fn should be something like apps.devmeta.core.helper.connect_sqlite
ConnectFn = Callable[[str], Any]


class TodoService:
    """
    Minimal TODO service for DevMeta MVP (SQLite).
    Provides add, list, and done operations on the 'todos' table.
    """

    def __init__(self, db_path: str, connect_fn: ConnectFn) -> None:
        self.db_path = db_path
        self.connect_fn = connect_fn

    def add(
        self,
        title: str,
        *,
        priority: int = 3,
        project: Optional[str] = None,
        due_at: Optional[str] = None,  # ISO or YYYY-MM-DD
    ) -> int:
        with self.connect_fn(self.db_path) as conn:
            conn.execute(
                "INSERT INTO todos(title, priority, project, due_at) VALUES (?, ?, ?, ?)",
                (title, priority, project, due_at),
            )
            row = conn.execute("SELECT last_insert_rowid() AS id").fetchone()
            todo_id = int(row["id"])
            LOG.info("todo_added", extra={"id": todo_id, "title": title})
            return todo_id

    def list(
        self,
        *,
        status: Optional[str] = None,
        project: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        q = ["SELECT * FROM todos"]
        conds: List[str] = []
        args: List[Any] = []

        if status:
            conds.append("status = ?")
            args.append(status)
        else:
            conds.append("status IN ('open','in_progress')")

        if project:
            conds.append("project = ?")
            args.append(project)

        if conds:
            q.append("WHERE " + " AND ".join(conds))

        q.append("ORDER BY (due_at IS NULL), due_at ASC, priority ASC, id ASC")
        if limit:
            q.append("LIMIT ?")
            args.append(limit)

        sql = " ".join(q)
        with self.connect_fn(self.db_path) as conn:
            rows = [dict(r) for r in conn.execute(sql, tuple(args)).fetchall()]
            return rows

    def done(self, todo_id: int) -> bool:
        now = datetime.now(UTC).isoformat(timespec="seconds")
        with self.connect_fn(self.db_path) as conn:
            cur = conn.execute(
                "UPDATE todos SET status='done', completed_at=?, updated_at=? WHERE id = ?",
                (now, now, todo_id),
            )
            ok = cur.rowcount > 0
            if ok:
                LOG.info("todo_completed", extra={"id": todo_id})
            else:
                LOG.warning("todo_complete_not_found", extra={"id": todo_id})
            return ok
