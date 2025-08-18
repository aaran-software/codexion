# apps/devmeta/models/todo.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Todo:
    """
    Represents a single TODO item in DevMeta.

    Fields align with the `todos` table created via migrations.
    """
    id: Optional[int] = None
    title: str = ""
    status: str = "pending"   # "pending", "in_progress", "done"
    priority: int = 0         # 0=normal, higher = more urgent
    project: Optional[str] = None

    due_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    def mark_done(self) -> None:
        """Mark this task as completed."""
        self.status = "done"
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def touch(self) -> None:
        """Update the `updated_at` timestamp."""
        self.updated_at = datetime.utcnow()

    def as_dict(self) -> dict:
        """Convert the Todo into a serializable dict."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
            "project": self.project,
            "due_at": self.due_at.isoformat() if self.due_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_row(cls, row: dict | tuple) -> "Todo":
        """
        Factory to build a Todo from a SQLite row (dict or tuple).
        Expects sqlite3.Row or raw tuple in SELECT order.
        """
        if isinstance(row, dict):
            return cls(
                id=row.get("id"),
                title=row.get("title", ""),
                status=row.get("status", "pending"),
                priority=row.get("priority", 0),
                project=row.get("project"),
                due_at=datetime.fromisoformat(row["due_at"]) if row.get("due_at") else None,
                created_at=datetime.fromisoformat(row["created_at"]) if row.get("created_at") else datetime.utcnow(),
                updated_at=datetime.fromisoformat(row["updated_at"]) if row.get("updated_at") else datetime.utcnow(),
                completed_at=datetime.fromisoformat(row["completed_at"]) if row.get("completed_at") else None,
            )
        else:
            # Assume tuple from SELECT * in order
            return cls(
                id=row[0],
                title=row[1],
                status=row[2],
                priority=row[3],
                project=row[4],
                due_at=datetime.fromisoformat(row[5]) if row[5] else None,
                created_at=datetime.fromisoformat(row[6]) if row[6] else datetime.utcnow(),
                updated_at=datetime.fromisoformat(row[7]) if row[7] else datetime.utcnow(),
                completed_at=datetime.fromisoformat(row[8]) if row[8] else None,
            )
