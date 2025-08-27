# prefiq/abstracts/page_controller.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

__all__ = ["APageController"]


class APageController(ABC):
    """Base for page controllers that render HTML/stream responses."""

    router: APIRouter

    def __init__(self, prefix: str = "", tags: Optional[list[str]] = None) -> None:
        self.router = APIRouter(prefix=prefix, tags=tags)
        self._register()

    @abstractmethod
    def route(self) -> str:
        ...

    @abstractmethod
    async def render(self, request: Request, **context: Any) -> Response:
        ...

    def _register(self) -> None:
        path = self.route() or "/"
        if not path.startswith("/"):
            path = "/" + path

        @self.router.get(path)
        async def _page(request: Request) -> Response:  # type: ignore[override]
            return await self.render(request)
