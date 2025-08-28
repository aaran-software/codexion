from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Mapping
from uuid import uuid4

from prefiq.contracts.IClock import SystemClock

@dataclass
class Entity:
    id: str = field(default_factory=lambda: str(uuid4()))
    tenant_id: str | None = None
    created_at: datetime = field(default_factory=lambda: SystemClock().now())
    updated_at: datetime = field(default_factory=lambda: SystemClock().now())
    # Extra fields are allowed via subclasses

    def validate(self) -> None:
        # Override in subclasses for richer validation
        if self.tenant_id is not None and not isinstance(self.tenant_id, str):
            raise ValueError("tenant_id must be a string or None")

    def touch(self) -> None:
        self.updated_at = SystemClock().now()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # datetime → isoformat for clean JSON interchange
        for k in ("created_at", "updated_at"):
            if isinstance(d.get(k), datetime):
                d[k] = d[k].isoformat()
        return d

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Entity":
        known = dict(data)
        for k in ("created_at", "updated_at"):
            v = known.get(k)
            if isinstance(v, str):
                known[k] = datetime.fromisoformat(v)
        return cls(**known)  # type: ignore[arg-type]
