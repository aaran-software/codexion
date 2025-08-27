# prefiq/contracts/repository.py
# =============================================

from __future__ import annotations
from typing import Protocol, Dict, Any, TypeVar, Generic, Iterable, Optional
from prefiq.contracts.model import IModel

TModel = TypeVar("TModel", bound=IModel)


class IRepository(Protocol, Generic[TModel]):
    def all(self) -> Iterable[TModel]:
        ...

    def paginate(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        ...

    def find(self, id: int) -> Optional[TModel]:
        ...

    def create(self, data: Dict[str, Any]) -> TModel:
        ...

    def update(self, id: int, data: Dict[str, Any]) -> Optional[TModel]:
        ...

    def delete(self, id: int) -> bool:
        ...
