from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, List
import json

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from prefiq.contracts.ITenantContext import TenantContext
from prefiq.http.deps import provide_context


def make_rest_router(
    resource: str,
    service: Any,   # Expected to implement: create(dict), get(id), update(id, dict), delete(id), list(page,size,filters,sort)
    *,
    tags: Optional[List[str]] = None,
) -> APIRouter:
    """
    Routes created under /{resource}:

      POST   /{resource}
      GET    /{resource}/{item_id}
      PATCH  /{resource}/{item_id}
      DELETE /{resource}/{item_id}
      GET    /{resource}  ?page=1&size=20&filters={}&sort=updated_at,-name
    """
    tags = tags or [resource]
    r = APIRouter()

    # ---- helpers ----
    def _to_plain_dict(obj: Any, where: str) -> Dict[str, Any]:
        """
        Coerce JSON-able bodies (Pydantic/Mapping/etc.) to a built-in dict with str keys.
        Some repos/drivers are strict and require type(data) is dict.
        """
        if isinstance(obj, dict):
            return {str(k): v for k, v in obj.items()}
        if isinstance(obj, Mapping):
            return {str(k): v for k, v in obj.items()}
        enc = jsonable_encoder(obj)
        if isinstance(enc, dict):
            return {str(k): v for k, v in enc.items()}
        raise HTTPException(status_code=400, detail=f"{where}: payload must be a JSON object")

    # ---- Create ----
    @r.post(f"/{resource}", tags=tags)
    def create_item(
        payload: Mapping[str, Any] = Body(...),
        ctx: TenantContext = Depends(provide_context),
    ) -> Dict[str, Any]:
        try:
            data = _to_plain_dict(payload, where="Create failed")
            return service.create(data)
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    # ---- Get ----
    @r.get(f"/{resource}/{{item_id}}", tags=tags)
    def get_item(
        item_id: str,
        ctx: TenantContext = Depends(provide_context),
    ) -> Dict[str, Any]:
        try:
            obj = service.get(item_id)
            if not obj:
                raise HTTPException(status_code=404, detail="Not found")
            return obj
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))

    # ---- Update (PATCH) ----
    @r.patch(f"/{resource}/{{item_id}}", tags=tags)
    def update_item(
        item_id: str,
        payload: Mapping[str, Any] = Body(...),
        ctx: TenantContext = Depends(provide_context),
    ) -> Dict[str, Any]:
        try:
            data = _to_plain_dict(payload, where="Update failed")
            return service.update(item_id, data)
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except KeyError:
            raise HTTPException(status_code=404, detail="Not found")
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    # ---- Delete ----
    @r.delete(f"/{resource}/{{item_id}}", tags=tags)
    def delete_item(
        item_id: str,
        ctx: TenantContext = Depends(provide_context),
    ) -> Dict[str, Any]:
        try:
            ok = service.delete(item_id)
            if not ok:
                raise HTTPException(status_code=404, detail="Not found")
            return {"ok": True}
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))

    # ---- List with pagination/filters/sort ----
    @r.get(f"/{resource}", tags=tags)
    def list_items(
        page: int = Query(1, ge=1),
        size: int = Query(20, ge=1, le=200),
        filters: Optional[str] = Query(None, description='JSON object, e.g. {"status":"done"}'),
        sort: Optional[str] = Query(None, description="CSV e.g. updated_at,-name"),
        ctx: TenantContext = Depends(provide_context),
    ) -> Dict[str, Any]:
        try:
            fdict: Optional[Dict[str, Any]] = None
            if filters:
                try:
                    fdict = json.loads(filters)
                    if not isinstance(fdict, dict):
                        raise ValueError("filters must be a JSON object")
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid filters JSON")
            slist: Optional[List[str]] = None
            if sort:
                slist = [s.strip() for s in sort.split(",") if s.strip()]
            return service.list(page=page, size=size, filters=fdict, sort=slist)
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))

    return r
