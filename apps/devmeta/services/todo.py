# apps/devmeta/services/todo.py

from __future__ import annotations

from datetime import datetime, UTC
from typing import Any, Callable, Optional, List, Union

from prefiq.log.logger import get_logger
from apps.devmeta.core.helper import connect_sqlite  # for binder

LOG = get_logger("prefiq.devmeta.service.todo")

# connect_fn should be something like apps.devmeta.core.helper.connect_sqlite
ConnectFn = Callable[[str], Any]

DueAtType = Optional[Union[str, datetime]]


def _normalize_due_at(due_at: DueAtType) -> Optional[str]:
    """
    Accepts a datetime (naive or aware), ISO string, or None.
    Returns an ISO 8601 string suitable for SQLite, or None.
    """
    if due_at is None:
        return None
    if isinstance(due_at, datetime):
        # keep seconds precision; always store as UTC ISO if aware
        if due_at.tzinfo is None:
            # assume local naive; keep as naive ISO to avoid surprise tz shifts
            return due_at.isoformat(timespec="seconds")
        return due_at.astimezone(UTC).isoformat(timespec="seconds")
    # string path
    try:
        # try robust parse via fromisoformat (supports 'YYYY-MM-DD' and full ISO)
        dt = datetime.fromisoformat(due_at)
        return _normalize_due_at(dt)
    except Exception:
        # last resort: store the raw string
        return str(due_at)


class TodoService:
    """
    Minimal TODO service for DevMeta (SQLite).
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
        due_at: DueAtType = None,   # accepts datetime | str | None
        tags: Optional[str] = None, # comma-separated tags
    ) -> Any:
        sql = (
            "INSERT INTO todos(title, priority, project, due_at, tags) "
            "VALUES (?, ?, ?, ?, ?)"
        )
        args = (title, priority, project, _normalize_due_at(due_at), tags)

        with self.connect_fn(self.db_path) as conn:
            conn.execute(sql, args)
            row = conn.execute("SELECT last_insert_rowid() AS id").fetchone()
            todo_id = int(row["id"])
            LOG.info("todo_added", extra={"id": todo_id, "title": title})
            return {"id": todo_id, "title": title}

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
            ok = (cur.rowcount or 0) > 0
            if ok:
                LOG.info("todo_completed", extra={"id": todo_id})
            else:
                LOG.warning("todo_complete_not_found", extra={"id": todo_id})
            return ok


# ---- Container binder (called by DevMetaProvider.register) ----

def bind_todo_service(app: Any, db_path: str) -> None:
    """
    Bind a TodoService instance into the DI container.

    Binds:
      - "devmeta.todo"  (namespaced)
      - "todo"          (short alias)
    """
    svc = TodoService(db_path=db_path, connect_fn=connect_sqlite)
    app.bind("devmeta.todo", svc)
    app.bind("todo", svc)
