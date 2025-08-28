from __future__ import annotations

from typing import Protocol, runtime_checkable, Mapping, Any, Dict, Generic, TypeVar

from .IDomain import IDomain

T = TypeVar("T", bound=IDomain)

@runtime_checkable
class IDomainService(Protocol, Generic[T]):
    def create(self, data: Mapping[str, Any]) -> Dict[str, Any]: ...
    def get(self, entity_id: str) -> Dict[str, Any] | None: ...
    def update(self, entity_id: str, data: Mapping[str, Any]) -> Dict[str, Any]: ...
    def delete(self, entity_id: str) -> bool: ...
    def list(
        self,
        page: int = 1,
        size: int = 20,
        filters: Mapping[str, Any] | None = None,
        sort: list[str] | None = None,
    ) -> Dict[str, Any]: ...
