from __future__ import annotations

from fastapi import Header, Depends
from typing import Optional
from prefiq.contracts.ITenantContext import TenantContext, set_current_context

def provide_context(
    x_tenant_id: Optional[str] = Header(default=None),
    x_user_id: Optional[str] = Header(default=None),
    x_roles: Optional[str] = Header(default=None),
) -> TenantContext:
    roles = frozenset({r.strip() for r in (x_roles or "").split(",") if r.strip()})
    ctx = TenantContext(tenant_id=x_tenant_id, user_id=x_user_id, roles=roles)
    set_current_context(ctx)
    return ctx
