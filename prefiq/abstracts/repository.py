# prefiq/abstracts/repository.py
from __future__ import annotations

from abc import ABC, abstractmethod
from threading import Lock
from typing import Any, Dict, Generic, Iterable, List, Optional, TypeVar

from .model import AModel

__all__ = ["ARepository"]

TModel = TypeVar("TModel", bound=AModel)


class ARepository(ABC, Generic[TModel]):
    """In-memory generic repository; override _build to construct TModel."""

    _auto_id: int

    def __init__(self) -> None:
        self._items: Dict[int, TModel] = {}
        self._auto_id = 1
        self._lock = Lock()

    def all(self) -> Iterable[TModel]:
        # snapshot to avoid mutation during iteration
        return list(self._items.values())

    def paginate(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        items: List[TModel] = list(self._items.values())
        total = len(items)
        start = max(0, (page - 1) * per_page)
        end = start + per_page
        return {
            "data": items[start:end],
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page if per_page else 1,
        }

    def find(self, item_id: int) -> Optional[TModel]:
        return self._items.get(item_id)

    def create(self, data: Dict[str, Any]) -> TModel:
        model = self._build(data)
        with self._lock:
            model.id = self._auto_id  # keep model attribute name as 'id'
            self._items[self._auto_id] = model
            self._auto_id += 1
        return model

    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[TModel]:
        if item_id not in self._items:
            return None
        current = self._items[item_id]
        updated = self._build({**current.to_dict(), **data, "id": item_id})
        # Defensive: ensure ID consistency
        if getattr(updated, "id", item_id) != item_id:
            setattr(updated, "id", item_id)
        with self._lock:
            self._items[item_id] = updated
        return updated

    def delete(self, item_id: int) -> bool:
        with self._lock:
            return self._items.pop(item_id, None) is not None

    @abstractmethod
    def _build(self, data: Dict[str, Any]) -> TModel:
        raise NotImplementedError
