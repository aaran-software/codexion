from __future__ import annotations

from typing import Protocol
from prefiq.contracts.ITenantContext import TenantContext

class Policy(Protocol):
    def can_create(self, ctx: TenantContext | None) -> bool: ...
    def can_read(self, ctx: TenantContext | None) -> bool: ...
    def can_update(self, ctx: TenantContext | None) -> bool: ...
    def can_delete(self, ctx: TenantContext | None) -> bool: ...

class AllowAllPolicy:
    def can_create(self, ctx): return True
    def can_read(self, ctx): return True
    def can_update(self, ctx): return True
    def can_delete(self, ctx): return True

class RolePolicy:
    """
    Simple role-gate: write needs 'editor' or 'admin'; read is open to all
    tenants; delete needs 'admin'.
    """
    def can_create(self, ctx: TenantContext | None) -> bool:
        return bool(ctx and (ctx.is_superuser or ctx.has_role("editor")))

    def can_read(self, ctx: TenantContext | None) -> bool:
        return ctx is not None

    def can_update(self, ctx: TenantContext | None) -> bool:
        return bool(ctx and (ctx.is_superuser or ctx.has_role("editor")))

    def can_delete(self, ctx: TenantContext | None) -> bool:
        return bool(ctx and ctx.is_superuser)
