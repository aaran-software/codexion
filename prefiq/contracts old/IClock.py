from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol

class IClock(Protocol):
    def now(self) -> datetime: ...

class SystemClock:
    def now(self) -> datetime:
        return datetime.now(timezone.utc)
