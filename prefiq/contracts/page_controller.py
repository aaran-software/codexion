# prefiq/contracts/page_controller.py
# =============================================

from __future__ import annotations

from typing import Protocol, Any
from starlette.requests import Request
from starlette.responses import Response


class IPageController(Protocol):
    """
    Contract for page (web) controllers that return rendered pages (HTML/stream/etc).
    """

    def route(self) -> str:
        """
        Return the route path this page is mounted at (e.g., "/" or "/dashboard").
        """
        ...

    async def render(self, request: Request, **context: Any) -> Response:
        """
        Produce a Response for the page. Implementors may use a templating engine
        or return raw HTMLResponse/StreamingResponse.
        """
        ...
