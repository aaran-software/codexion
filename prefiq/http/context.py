# prefiq/http/context.py

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Iterable, Optional, Set, List, AsyncGenerator


# ----- in-request context ----------------------------------------------------

@dataclass
class RequestContext:
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    roles: Set[str] = frozenset()

_ctx: ContextVar[Optional[RequestContext]] = ContextVar("prefiq_ctx", default=None)

def get_current_context() -> Optional[RequestContext]:
    """Return the current RequestContext (or None outside of a request)."""
    return _ctx.get()

def set_current_context(ctx: Optional[RequestContext]) -> None:
    """
    Imperatively set the current RequestContext. Useful for adapters that already
    parsed headers (or tests). This does NOT return the token; for scoped use,
    prefer bind_request_context().
    """
    _ctx.set(ctx)

def _normalize_roles(roles: Iterable[str] | str | None) -> Set[str]:
    if not roles:
        return set()
    if isinstance(roles, str):
        parts = [r.strip() for r in roles.split(",")]
    else:
        parts = [str(r).strip() for r in roles]
    return {p for p in parts if p}

def has_role(role: str) -> bool:
    ctx = get_current_context()
    return bool(ctx and role in (ctx.roles or set()))

@contextmanager
def bind_request_context(
    tenant_id: Optional[str],
    user_id: Optional[str],
    roles: Iterable[str] | str | None,
):
    """
    Context-manager to bind a RequestContext for the duration of a block.
    Useful in tests or imperative code.
    """
    token = _ctx.set(RequestContext(
        tenant_id=tenant_id,
        user_id=user_id,
        roles=_normalize_roles(roles),
    ))
    try:
        yield _ctx.get()
    finally:
        _ctx.reset(token)

# ----- FastAPI-friendly dependency (optional) -------------------------------

try:
    # Don't make FastAPI a hard dependency of this module;
    # expose the dependency only if FastAPI is available.
    from fastapi import Header


    async def request_context_dependency(
            x_tenant_id: Optional[str] = Header(default=None, alias="X-Tenant-ID"),
            x_user_id: Optional[str] = Header(default=None, alias="X-User-ID"),
            x_roles: Optional[str] = Header(default="", alias="X-Roles"),
    ) -> AsyncGenerator[RequestContext, None]:
        """
        FastAPI dependency: binds headers into RequestContext for this request.
        Keeps the context active during the handler, then cleans up.
        """
        token = _ctx.set(RequestContext(
            tenant_id=x_tenant_id,
            user_id=x_user_id,
            roles=_normalize_roles(x_roles),
        ))
        try:
            yield _ctx.get() or RequestContext()
        finally:
            _ctx.reset(token)

except Exception:
    # If FastAPI isn't installed in some environments, it's fine —
    # users can still use bind_request_context() directly.
    pass

__all__ = [
    "RequestContext",
    "get_current_context",
    "set_current_context",
    "bind_request_context",
    "has_role",
    "request_context_dependency",
]
