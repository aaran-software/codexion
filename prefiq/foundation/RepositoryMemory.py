from __future__ import annotations

from typing import Dict, Any, Mapping, Generic, TypeVar, Iterable

from prefiq.contracts.IDomain import IDomain
from prefiq.foundation.Mapper import Mapper
from prefiq.foundation.Pagination import PagedResult

T = TypeVar("T", bound=IDomain)

class MemoryRepository(Generic[T]):
    """
    In-memory, tenant-scoped repository. Perfect for dev/tests.
    """

    def __init__(self, mapper: Mapper[T]) -> None:
        self._mapper = mapper
        self._store: Dict[str, Dict[str, Dict[str, Any]]] = {}  # tenant -> id -> record

    def _bucket(self, tenant_id: str | None) -> Dict[str, Dict[str, Any]]:
        key = tenant_id or "_global"
        return self._store.setdefault(key, {})

    # CRUD
    def create(self, entity: T) -> Dict[str, Any]:
        rec = self._mapper.to_record(entity)
        self._bucket(entity.tenant_id)[entity.id] = rec
        return rec

    def get(self, tenant_id: str | None, entity_id: str) -> Dict[str, Any] | None:
        return self._bucket(tenant_id).get(entity_id)

    def update(self, entity: T) -> Dict[str, Any]:
        rec = self._mapper.to_record(entity)
        self._bucket(entity.tenant_id)[entity.id] = rec
        return rec

    def delete(self, tenant_id: str | None, entity_id: str) -> bool:
        return self._bucket(tenant_id).pop(entity_id, None) is not None

    def list(
        self,
        tenant_id: str | None,
        page: int,
        size: int,
        filters: Mapping[str, Any] | None,
        sort: list[str] | None,
    ) -> PagedResult[Dict[str, Any]]:
        bucket = list(self._bucket(tenant_id).values())

        # naive filter: exact match on top-level keys
        if filters:
            def keep(r: Dict[str, Any]) -> bool:
                return all(r.get(k) == v for k, v in filters.items())
            bucket = [r for r in bucket if keep(r)]

        # naive sort: prefix '-' for desc
        if sort:
            for key in reversed(sort):
                rev = key.startswith("-")
                k = key[1:] if rev else key
                bucket.sort(key=lambda r: r.get(k), reverse=rev)

        total = len(bucket)
        start = max(0, (max(1, page) - 1) * max(1, size))
        end = start + size
        items = bucket[start:end]
        return PagedResult(items=items, total=total, page=page, size=size)
