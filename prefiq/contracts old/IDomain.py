from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Mapping, Any, Dict, Type, TypeVar

T_IDomain = TypeVar("T_IDomain", bound="IDomain")

@runtime_checkable
class IDomain(Protocol):
    id: str
    tenant_id: str | None

    def validate(self) -> None: ...
    def to_dict(self) -> Dict[str, Any]: ...

    @classmethod
    def from_dict(cls: Type[T_IDomain], data: Mapping[str, Any]) -> T_IDomain: ...
