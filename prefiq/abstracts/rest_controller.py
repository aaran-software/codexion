# prefiq/abstracts/rest_controller.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type

from fastapi import APIRouter, Body, HTTPException

__all__ = ["ARestController"]


class ARestController(ABC):
    """
    Base CRUD router; subclass and implement handlers.
    Optionally provide Pydantic models via class attrs to enrich OpenAPI.
    """

    # Optional Pydantic schemas for better OpenAPI (set in subclasses)
    create_model: Optional[Type[Any]] = None
    update_model: Optional[Type[Any]] = None
    read_model: Optional[Type[Any]] = None
    list_model: Optional[Type[Any]] = None

    router: APIRouter

    def __init__(self, prefix: str = "", tags: Optional[list[str]] = None) -> None:
        self.router = APIRouter(prefix=prefix, tags=tags)
        self._register()

    # ---- Abstract handlers ----
    @abstractmethod
    def index(self, page: int = 1, per_page: int = 20) -> Any: ...
    @abstractmethod
    def show(self, item_id: int) -> Any: ...
    @abstractmethod
    def store(self, payload: Dict[str, Any]) -> Any: ...
    @abstractmethod
    def update(self, item_id: int, payload: Dict[str, Any]) -> Any: ...
    @abstractmethod
    def destroy(self, item_id: int) -> bool | None: ...

    # ---- Route wiring ----
    def _register(self) -> None:
        read_model = self.read_model
        list_model = self.list_model

        @self.router.get("/", response_model=list_model)  # type: ignore[arg-type]
        def _index(page: int = 1, per_page: int = 20):
            return self.index(page=page, per_page=per_page)

        @self.router.get("/{item_id}", response_model=read_model)  # type: ignore[arg-type]
        def _show(item_id: int):
            result = self.show(item_id)
            if result is None:
                raise HTTPException(status_code=404, detail="Resource not found")
            return result

        # Use provided Pydantic model for request if available, else accept Dict
        if self.create_model is not None:
            create_model = self.create_model  # lowercase variable name

            @self.router.post("/", status_code=201, response_model=read_model)  # type: ignore[arg-type]
            def _store(payload: create_model):  # type: ignore[valid-type]
                return self.store(payload.dict())  # type: ignore[attr-defined]
        else:

            @self.router.post("/", status_code=201, response_model=read_model)  # type: ignore[arg-type]
            def _store(payload: Dict[str, Any] = Body(...)):
                return self.store(payload)

        if self.update_model is not None:
            update_model = self.update_model  # lowercase variable name

            @self.router.put("/{item_id}", response_model=read_model)  # type: ignore[arg-type]
            def _update(item_id: int, payload: update_model):  # type: ignore[valid-type]
                result = self.update(item_id, payload.dict())  # type: ignore[attr-defined]
                if result is None:
                    raise HTTPException(status_code=404, detail="Resource not found")
                return result
        else:

            @self.router.put("/{item_id}", response_model=read_model)  # type: ignore[arg-type]
            def _update(item_id: int, payload: Dict[str, Any] = Body(...)):
                result = self.update(item_id, payload)
                if result is None:
                    raise HTTPException(status_code=404, detail="Resource not found")
                return result

        @self.router.delete("/{item_id}", status_code=204)
        def _destroy(item_id: int):
            ok = self.destroy(item_id)
            if not ok:
                raise HTTPException(status_code=404, detail="Resource not found")
            return None
