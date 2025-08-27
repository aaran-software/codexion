# prefiq/contracts/model.py
# =============================================

from __future__ import annotations
from typing import Protocol, Dict, Any, TypeVar, Optional


class IModel(Protocol):
    id: Optional[int]

    def to_dict(self) -> Dict[str, Any]:
        ...

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IModel":
        ...


TModel = TypeVar("TModel", bound=IModel)
