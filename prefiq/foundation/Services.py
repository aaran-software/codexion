from __future__ import annotations

from typing import Generic, TypeVar, Mapping, Any, Dict, Callable

from prefiq.contracts.IDomain import IDomain
from prefiq.contracts.IDomainService import IDomainService
from prefiq.contracts.ITenantContext import get_current_context, TenantContext
from prefiq.contracts.IClock import SystemClock
from prefiq.foundation.Hooks import HookRegistry, HookNames
from prefiq.foundation.Events import DomainEvent, global_bus
from prefiq.foundation.Pagination import PagedResult

T = TypeVar("T", bound=IDomain)

class BaseDomainService(Generic[T], IDomainService[T]):
    """
    Storage-agnostic, JSON-first service:
    - Validates
    - Enforces basic policies
    - Fires hooks/events
    - Returns dicts ready for JSON
    """

    def __init__(
        self,
        *,
        entity_ctor: type[T],
        repository: Any,                       # MemoryRepository or SqlRepository
        policy: Any,                           # Policy or compatible object
        hooks: HookRegistry[T] | None = None,
        publish_events: bool = True,
        event_prefix: str = "",
    ) -> None:
        self.entity_ctor = entity_ctor
        self.repo = repository
        self.policy = policy
        self.hooks = hooks or HookRegistry[T]()
        self.publish_events = publish_events
        self.event_prefix = event_prefix

    # --- helpers ---
    def _ctx(self) -> TenantContext | None:
        return get_current_context()

    def _ensure(self, ok: bool, msg: str) -> None:
        if not ok:
            raise PermissionError(msg)

    def _emit(self, name: str, payload: Dict[str, Any]) -> None:
        if self.publish_events:
            global_bus.publish(DomainEvent(name=name, payload=payload))

    # --- IDomainService ---
    def create(self, data: Mapping[str, Any]) -> Dict[str, Any]:
        ctx = self._ctx()
        self._ensure(self.policy.can_create(ctx), "Not allowed to create.")
        entity = self.entity_ctor.from_dict(dict(data))
        if ctx and getattr(entity, "tenant_id", None) is None:
            entity.tenant_id = ctx.tenant_id  # type: ignore[attr-defined]
        entity.validate()
        self.hooks.run(HookNames.BEFORE_CREATE, entity)
        out = self.repo.create(entity)
        self.hooks.run(HookNames.AFTER_CREATE, entity)
        self._emit(self.event_prefix + "created", {"id": out["id"], "tenant_id": out.get("tenant_id")})
        return out

    def get(self, entity_id: str) -> Dict[str, Any] | None:
        ctx = self._ctx()
        self._ensure(self.policy.can_read(ctx), "Not allowed to read.")
        return self.repo.get(ctx.tenant_id if ctx else None, entity_id)

    def update(self, entity_id: str, data: Mapping[str, Any]) -> Dict[str, Any]:
        ctx = self._ctx()
        self._ensure(self.policy.can_update(ctx), "Not allowed to update.")
        current = self.get(entity_id)
        if not current:
            raise KeyError("Not found")
        merged = dict(current) | dict(data)
        entity = self.entity_ctor.from_dict(merged)
        if ctx and getattr(entity, "tenant_id", None) is None:
            entity.tenant_id = ctx.tenant_id  # type: ignore[attr-defined]
        entity.touch()
        entity.validate()
        self.hooks.run(HookNames.BEFORE_UPDATE, entity)
        out = self.repo.update(entity)
        self.hooks.run(HookNames.AFTER_UPDATE, entity)
        self._emit(self.event_prefix + "updated", {"id": out["id"]})
        return out

    def delete(self, entity_id: str) -> bool:
        ctx = self._ctx()
        self._ensure(self.policy.can_delete(ctx), "Not allowed to delete.")
        ok = self.repo.delete(ctx.tenant_id if ctx else None, entity_id)
        if ok:
            self._emit(self.event_prefix + "deleted", {"id": entity_id})
        return ok

    def list(
        self,
        page: int = 1,
        size: int = 20,
        filters: Mapping[str, Any] | None = None,
        sort: list[str] | None = None,
    ) -> Dict[str, Any]:
        ctx = self._ctx()
        self._ensure(self.policy.can_read(ctx), "Not allowed to read.")
        paged: PagedResult[Dict[str, Any]] = self.repo.list(
            ctx.tenant_id if ctx else None, page, size, filters, sort
        )
        return paged.to_dict()
