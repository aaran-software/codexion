from __future__ import annotations

import json
import os
from inspect import signature
from typing import Any, Dict, List, Mapping, Optional

from collections.abc import Mapping as AbcMapping
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.encoders import jsonable_encoder

from prefiq.database import get_engine
# Service layer
from .service import get_service, guarded_update

# Bind request headers (X-Tenant-ID, X-User-ID, X-Roles) into Prefiq context if available
try:
    from prefiq.http.context import request_context_dependency as inject_ctx
except Exception:  # fallback: no-op dependency
    async def inject_ctx() -> None:
        return None

# Provider mounts with prefix="/api" ⇒ final routes under /api/projects/...
router = APIRouter(prefix="/projects", tags=["projects"])

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _to_plain_dict(obj: Any, *, where: str) -> Dict[str, Any]:
    """
    Coerce various JSON-able bodies (pydantic/BaseModel/Mapping) into a built-in dict.
    Some repos check `type(data) is dict` rather than `isinstance`, so be strict here.
    """
    if isinstance(obj, dict):
        return {str(k): v for k, v in obj.items()}
    if isinstance(obj, AbcMapping):
        return {str(k): v for k, v in obj.items()}
    enc = jsonable_encoder(obj)
    if isinstance(enc, dict):
        return {str(k): v for k, v in enc.items()}
    raise HTTPException(status_code=400, detail=f"{where}: payload must be a JSON object")

# ─────────────────────────────────────────────────────────────────────────────
# Create
# ─────────────────────────────────────────────────────────────────────────────

@router.post("", summary="Create a project")
def create_project(
    payload: Dict[str, Any] = Body(...),
    _ctx: Optional[Any] = Depends(inject_ctx),
):
    """
    Accepts a JSON object like:
    {
      "name": "...",
      "status": "...", "priority": "...",
      "tags": [...], "meta": {...},
      "description": "...",
      "start_date": "YYYY-MM-DD",
      "due_date":   "YYYY-MM-DD"
    }
    """
    try:
        data = _to_plain_dict(payload, where="Create failed")
        svc = get_service()
        result = svc.create(data)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Create failed: {e}")

    if isinstance(result, dict):
        return result
    return {"id": result, "ok": True}

# ─────────────────────────────────────────────────────────────────────────────
# Read (by id)
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/{project_id}", response_model=Dict[str, Any])
def get_project(
    project_id: str,
    _ctx: Optional[Any] = Depends(inject_ctx),
):
    svc = get_service()
    try:
        obj = svc.get(project_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return obj
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

# ─────────────────────────────────────────────────────────────────────────────
# List (pagination / filters / sort)
# ─────────────────────────────────────────────────────────────────────────────

@router.get("", response_model=Dict[str, Any])
def list_projects(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    filters: Optional[str] = Query(None, description='JSON string like {"status":"new"}'),
    sort: Optional[str] = Query(None, description="Comma-separated fields; prefix with - for desc"),
    _ctx: Optional[Any] = Depends(inject_ctx),
):
    svc = get_service()
    fdict: Optional[Dict[str, Any]] = None
    if filters:
        try:
            fdict = json.loads(filters)
            if not isinstance(fdict, dict):
                fdict = None
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid filters JSON")
    slist: Optional[List[str]] = None
    if sort:
        slist = [s.strip() for s in sort.split(",") if s.strip()]
    try:
        return svc.list(page=page, size=size, filters=fdict, sort=slist)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

# ─────────────────────────────────────────────────────────────────────────────
# Update (guarded)
# ─────────────────────────────────────────────────────────────────────────────

@router.patch("/{project_id}", response_model=Dict[str, Any])
def update_project(
    project_id: str,
    payload: Mapping[str, Any] = Body(...),
    _ctx: Optional[Any] = Depends(inject_ctx),
):
    try:
        data = _to_plain_dict(payload, where="Update failed")
        return guarded_update(project_id, data)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="Not found")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

# ─────────────────────────────────────────────────────────────────────────────
# Transition
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/{project_id}/transition", response_model=Dict[str, Any])
def transition_project(
    project_id: str,
    payload: Mapping[str, Any] = Body(...),
    _ctx: Optional[Any] = Depends(inject_ctx),
):
    data = _to_plain_dict(payload, where="Transition failed")
    to_status = (data or {}).get("to")
    svc = get_service()
    try:
        return svc.transition(project_id, to_status)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="Not found")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

# ─────────────────────────────────────────────────────────────────────────────
# Delete
# ─────────────────────────────────────────────────────────────────────────────

@router.delete("/{project_id}", response_model=Dict[str, Any])
def delete_project(
    project_id: str,
    _ctx: Optional[Any] = Depends(inject_ctx),
):
    svc = get_service()
    try:
        ok = svc.delete(project_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Not found")
        return {"ok": True}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

# ─────────────────────────────────────────────────────────────────────────────
# Debug (optional)
# ─────────────────────────────────────────────────────────────────────────────

if os.environ.get("PREFIQ_DEBUG_ROUTES") == "1":
    @router.get("/_debug/ctx")
    def debug_ctx(_ctx: Optional[Any] = Depends(inject_ctx)):
        from prefiq.http.context import get_current_context
        ctx = get_current_context()
        return {
            "tenant_id": getattr(ctx, "tenant_id", None),
            "user_id": getattr(ctx, "user_id", None),
            "roles": list(getattr(ctx, "roles", [])),
        }

    @router.get("/_debug/engine")
    def debug_engine():
        eng = get_engine()
        try:
            sig = str(signature(getattr(eng, "execute")))
        except Exception:
            sig = "<unavailable>"
        return {
            "engine_class": type(eng).__name__,
            "module": type(eng).__module__,
            "execute_signature": sig,
        }