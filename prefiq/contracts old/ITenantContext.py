from __future__ import annotations
from dataclasses import dataclass, field
from contextvars import ContextVar
from typing import Iterable, Optional

@dataclass(frozen=True)
class TenantContext:
    tenant_id: str | None
    user_id: str | None
    roles: frozenset[str] = field(default_factory=frozenset)

    def has_role(self, *names: str) -> bool:
        # case-insensitive match
        want = {n.lower() for n in names}
        mine = {r.lower() for r in self.roles}
        return bool(want & mine)

    @property
    def is_superuser(self) -> bool:
        mine = {r.lower() for r in self.roles}
        return "admin" in mine or "superuser" in mine

# Primary context var
_current_ctx: ContextVar[TenantContext | None] = ContextVar("prefiq_tenant_ctx", default=None)

# Fallback for thread pool / sync handlers
_legacy_ctx: TenantContext | None = None

def set_current_context(ctx: TenantContext | None) -> None:
    """Set both ContextVar and a legacy global fallback (for thread-pool executed sync routes)."""
    global _legacy_ctx
    _current_ctx.set(ctx)
    _legacy_ctx = ctx

def get_current_context() -> TenantContext | None:
    """Read ContextVar; if empty, use the fallback set during dependency resolution."""
    ctx = _current_ctx.get()
    return ctx if ctx is not None else _legacy_ctx
