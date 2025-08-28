from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, DefaultDict, Dict, List
from collections import defaultdict
from prefiq.contracts.IClock import SystemClock

@dataclass(frozen=True)
class DomainEvent:
    name: str
    payload: Dict[str, Any] = field(default_factory=dict)
    ts: datetime = field(default_factory=lambda: SystemClock().now())

class EventBus:
    def __init__(self) -> None:
        self._subs: DefaultDict[str, List[Callable[[DomainEvent], None]]] = defaultdict(list)

    def subscribe(self, name: str, handler: Callable[[DomainEvent], None]) -> None:
        self._subs[name].append(handler)

    def publish(self, event: DomainEvent) -> None:
        for h in list(self._subs.get(event.name, [])):
            h(event)

global_bus = EventBus()
