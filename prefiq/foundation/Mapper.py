from __future__ import annotations

from typing import TypeVar, Generic, Mapping, Any, Dict

from prefiq.contracts.IDomain import IDomain

T = TypeVar("T", bound=IDomain)

class Mapper(Generic[T]):
    """
    Default mapper: entity <-> plain dict (JSON-friendly).
    Override to customize field transforms or DB column mapping.
    """

    def to_record(self, entity: T) -> Dict[str, Any]:
        return entity.to_dict()

    def from_record(self, data: Mapping[str, Any], ctor: type[T]) -> T:
        return ctor.from_dict(data)
