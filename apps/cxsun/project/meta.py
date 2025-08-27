from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any, Dict, List, Optional

STATUSES = ("new", "in_progress", "done", "archived")
PRIORITIES = ("low", "normal", "high")


def now_sql() -> str:
    # timezone-aware UTC formatted for SQL text fields
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")


def normalize_status(value: Optional[str]) -> str:
    v = (value or "new").strip().lower()
    if v not in STATUSES:
        raise ValueError("Invalid status")
    return v


def normalize_priority(value: Optional[str]) -> str:
    v = (value or "normal").strip().lower()
    if v not in PRIORITIES:
        raise ValueError("Invalid priority")
    return v


def can_transition(src: str, dst: str) -> bool:
    if src == "archived":  # no transitions out of archived
        return False
    allowed = {
        "new": {"in_progress"},
        "in_progress": {"done"},
        "done": {"archived"},
    }
    return dst in allowed.get(src, set())


@dataclass
class Project:
    id: Optional[str]
    tenant_id: Optional[str]
    name: str
    status: str = "new"
    owner_id: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None  # 'YYYY-MM-DD'
    due_date: Optional[str] = None    # 'YYYY-MM-DD'
    priority: str = "normal"
    tags: Optional[List[str]] = field(default_factory=list)
    meta: Optional[Dict[str, Any]] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def validate(self) -> None:
        self.status = normalize_status(self.status)
        self.priority = normalize_priority(self.priority)
        if self.start_date and self.due_date and self.start_date > self.due_date:
            raise ValueError("due_date must be >= start_date")

    def touch(self) -> None:
        self.updated_at = now_sql()

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Project":
        return cls(
            id=d.get("id"),
            tenant_id=d.get("tenant_id"),
            name=d.get("name", ""),
            status=d.get("status", "new"),
            owner_id=d.get("owner_id"),
            description=d.get("description"),
            start_date=d.get("start_date"),
            due_date=d.get("due_date"),
            priority=d.get("priority", "normal"),
            tags=d.get("tags") or [],
            meta=d.get("meta") or {},
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "status": self.status,
            "owner_id": self.owner_id,
            "description": self.description,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "priority": self.priority,
            "tags": self.tags,
            "meta": self.meta,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
