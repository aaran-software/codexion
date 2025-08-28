# prefiq/contracts/service.py
# =============================================

from __future__ import annotations
from typing import Protocol, Dict, Any, Iterable, Optional, TypeVar
from .repository import IRepository
from .model import IModel

TModel = TypeVar("TModel", bound=IModel)


class IService(Protocol[TModel]):
    repository: IRepository[TModel]

    def list(self) -> Iterable[TModel]:
        ...

    def paginate(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        ...

    def get(self, item_id: int) -> Optional[TModel]:
        ...

    def create(self, data: Dict[str, Any]) -> TModel:
        ...

    def update(self, item_id: int, data: Dict[str, Any]) -> Optional[TModel]:
        ...

    def delete(self, item_id: int) -> bool:
        ...
