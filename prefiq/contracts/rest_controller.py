# prefiq/contracts/rest_controller.py
# =============================================

from __future__ import annotations
from typing import Protocol, Dict, Any


class IRestController(Protocol):
    def index(self, page: int = 1, per_page: int = 20):
        ...

    def show(self, item_id: int):
        ...

    def store(self, payload: Dict[str, Any]):
        ...

    def update(self, item_id: int, payload: Dict[str, Any]):
        ...

    def destroy(self, item_id: int):
        ...
