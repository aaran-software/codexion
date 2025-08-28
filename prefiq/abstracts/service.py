# prefiq/abstracts/service.py
from __future__ import annotations

from abc import ABC
from typing import Any, Dict, Generic, Iterable, Optional, TypeVar

from .repository import ARepository
from .model import AModel

__all__ = ["AService"]

TModel = TypeVar("TModel", bound=AModel)


class AService(ABC, Generic[TModel]):
    """Thin domain service with validate/before/after hooks."""

    def __init__(self, repository: ARepository[TModel]):
        self.repository = repository

    # Shared validation hook (override as needed)
    @staticmethod
    def validate(data: Dict[str, Any]) -> Dict[str, Any]:
        return data

    # Hooks for business rules / policies
    @staticmethod
    def before_create(data: Dict[str, Any]) -> Dict[str, Any]:
        return data

    @staticmethod
    def after_create(model: TModel) -> TModel:
        return model

    @staticmethod
    def before_update(_item_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return data

    @staticmethod
    def after_update(model: TModel) -> TModel:
        return model

    # Public API
    def list(self) -> Iterable[TModel]:
        return self.repository.all()

    def paginate(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        return self.repository.paginate(page, per_page)

    def get(self, item_id: int) -> Optional[TModel]:
        return self.repository.find(item_id)

    def create(self, data: Dict[str, Any]) -> TModel:
        data = self.validate(data)
        data = self.before_create(data)
        model = self.repository.create(data)
        return self.after_create(model)

    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[TModel]:
        data = self.validate(data)
        data = self.before_update(item_id, data)
        model = self.repository.update(item_id, data)
        return None if model is None else self.after_update(model)

    def delete(self, item_id: int) -> bool:
        return self.repository.delete(item_id)
