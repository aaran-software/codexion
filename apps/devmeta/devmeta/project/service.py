# apps/devmeta/devmeta/project/service.py

from __future__ import annotations
from typing import Any, Dict, Mapping, Optional, List
from prefiq.http.context import get_current_context
from .repo_core import DBRepository
from .repo_utils import roles_set

_repo_singleton: Optional[DBRepository] = None

def get_repo() -> DBRepository:
    global _repo_singleton
    if _repo_singleton is None:
        _repo_singleton = DBRepository()
    return _repo_singleton

class Service:
    def __init__(self, repo: DBRepository) -> None:
        self.repo = repo

    def create(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        ctx = get_current_context()
        rs = roles_set(ctx)
        if "admin" not in rs and "editor" not in rs:
            raise PermissionError("Not allowed to create.")
        return self.repo.create(payload)

    def get(self, entity_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.get(entity_id)

    def list(self, *, page: int, size: int, filters: Optional[Mapping[str, Any]], sort: Optional[List[str]]) -> Dict[str, Any]:
        return self.repo.list(page=page, size=size, filters=filters, sort=sort)

    def update(self, entity_id: str, patch: Mapping[str, Any]) -> Dict[str, Any]:
        return self.repo.update(entity_id, patch)

    def delete(self, entity_id: str) -> bool:
        ctx = get_current_context()
        rs = roles_set(ctx)
        if "admin" not in rs:
            raise PermissionError("Not allowed to delete.")
        return self.repo.delete(entity_id)

    def transition(self, entity_id: str, to_status: Optional[str]) -> Dict[str, Any]:
        ctx = get_current_context()
        rs = roles_set(ctx)
        if "admin" in rs:
            return self.repo.transition(entity_id, to_status)
        cur = self.repo.get(entity_id)
        if not cur:
            raise KeyError("Not found")
        if cur.get("owner_id") and cur.get("owner_id") != getattr(ctx, "user_id", None):
            raise PermissionError("Not allowed to transition row you do not own.")
        return self.repo.transition(entity_id, to_status)

def get_service() -> Service:
    return Service(get_repo())

def guarded_update(entity_id: str, patch: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Owner-only update unless admin.
    """
    svc = get_service()
    ctx = get_current_context()
    rs = roles_set(ctx)
    if "admin" in rs:
        return svc.update(entity_id, patch)

    cur = svc.get(entity_id)
    if not cur:
        raise KeyError("Not found")

    if cur.get("owner_id") and cur.get("owner_id") != getattr(ctx, "user_id", None):
        raise PermissionError("Not allowed to update row you do not own.")

    if "owner_id" in patch:
        raise PermissionError("Not allowed to change owner_id.")

    return svc.update(entity_id, patch)
