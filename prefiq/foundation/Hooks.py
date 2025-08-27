from __future__ import annotations

from typing import Callable, TypeVar, Generic, Dict, List, Protocol
from prefiq.contracts.IDomain import IDomain

T = TypeVar("T", bound=IDomain)

class HookNames:
    BEFORE_CREATE = "before_create"
    AFTER_CREATE = "after_create"
    BEFORE_UPDATE = "before_update"
    AFTER_UPDATE = "after_update"
    BEFORE_DELETE = "before_delete"
    AFTER_DELETE = "after_delete"

Hook = Callable[[T], None]

class HookRegistry(Generic[T]):
    def __init__(self) -> None:
        self._hooks: Dict[str, List[Hook[T]]] = {
            HookNames.BEFORE_CREATE: [],
            HookNames.AFTER_CREATE: [],
            HookNames.BEFORE_UPDATE: [],
            HookNames.AFTER_UPDATE: [],
            HookNames.BEFORE_DELETE: [],
            HookNames.AFTER_DELETE: [],
        }

    def on(self, name: str, fn: Hook[T]) -> None:
        self._hooks[name].append(fn)

    def run(self, name: str, entity: T) -> None:
        for fn in self._hooks.get(name, []):
            fn(entity)
