from __future__ import annotations
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple
import uuid
from dataclasses import asdict

from prefiq.http.context import get_current_context
from prefiq.database import get_engine
from .meta import now_sql, Project, can_transition
from .repo_utils import adapt_params_for_engine, dumps_json, loads_json, roles_set
# If you already have is_mariadb_engine in repo_utils, import it; otherwise inline a tiny helper:
try:
    from .repo_utils import is_mariadb_engine  # type: ignore
except Exception:
    def is_mariadb_engine(engine) -> bool:
        return "mariadb" in (type(engine).__module__ or "").lower()

TABLE = "projects"
COLUMNS: List[str] = [
    "id", "tenant_id", "name", "status", "owner_id",
    "description", "start_date", "due_date", "priority",
    "tags", "meta", "created_at", "updated_at",
]

def _row_to_dict(row: Iterable[Any]) -> Dict[str, Any]:
    tup = list(row)
    out: Dict[str, Any] = dict(zip(COLUMNS, tup))
    out["tags"] = loads_json(out.get("tags"))
    out["meta"] = loads_json(out.get("meta"))
    return out

class DBRepository:
    TABLE = "projects"

    def _exec(self, sql: str, params: Optional[Mapping[str, Any]] = None):
        eng = get_engine()
        sql2, p2 = adapt_params_for_engine(eng, sql, params)
        return eng.execute(sql2) if p2 is None else eng.execute(sql2, p2)

    def _fetchone(self, sql: str, params: Optional[Mapping[str, Any]] = None) -> Optional[Dict[str, Any]]:
        eng = get_engine()
        sql2, p2 = adapt_params_for_engine(eng, sql, params)
        row = eng.fetchone(sql2) if p2 is None else eng.fetchone(sql2, p2)
        if not row:
            return None
        return _row_to_dict(row)

    def _fetchall(self, sql: str, params: Optional[Mapping[str, Any]] = None) -> List[Dict[str, Any]]:
        eng = get_engine()
        sql2, p2 = adapt_params_for_engine(eng, sql, params)
        rows = eng.fetchall(sql2) if p2 is None else eng.fetchall(sql2, p2)
        return [_row_to_dict(r) for r in rows]
    # ──────────────────────────────────────────────────────────────────────
    # CRUD / workflow
    # ──────────────────────────────────────────────────────────────────────
    def create(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        ctx = get_current_context()
        tenant_id = getattr(ctx, "tenant_id", None)
        owner_id = getattr(ctx, "user_id", None)

        if hasattr(Project, "from_payload"):
            p = Project.from_payload(payload)  # type: ignore[attr-defined]
            p.id = p.id or str(uuid.uuid4())
            p.tenant_id = p.tenant_id or tenant_id
            p.owner_id = p.owner_id or owner_id
            p.created_at = p.created_at or now_sql()
            p.updated_at = now_sql()
            p.tags = dumps_json(p.tags)
            p.meta = dumps_json(p.meta)
            row = asdict(p)
        else:
            name = str(payload.get("name") or "").strip()
            if not name:
                raise ValueError("name is required")
            row = {
                "id": str(uuid.uuid4()),
                "tenant_id": tenant_id,
                "name": name,
                "status": (payload.get("status") or "new").strip().lower(),
                "owner_id": owner_id,
                "description": payload.get("description"),
                "start_date": payload.get("start_date"),
                "due_date": payload.get("due_date"),
                "priority": (payload.get("priority") or "normal").strip().lower(),
                "tags": dumps_json(payload.get("tags")),
                "meta": dumps_json(payload.get("meta")),
                "created_at": now_sql(),
                "updated_at": now_sql(),
            }

        cols = ", ".join(COLUMNS)
        placeholders = ", ".join([f":{c}" for c in COLUMNS])
        sql = f"INSERT INTO {self.TABLE} ({cols}) VALUES ({placeholders})"
        self._exec(sql, row)
        return self.get(row["id"]) or row

    def get(self, entity_id: str) -> Optional[Dict[str, Any]]:
        ctx = get_current_context()
        tenant_id = getattr(ctx, "tenant_id", None)
        sql = f"SELECT {', '.join(COLUMNS)} FROM {self.TABLE} WHERE id=:id AND (tenant_id IS NULL OR tenant_id=:tenant_id)"
        return self._fetchone(sql, {"id": entity_id, "tenant_id": tenant_id})

    def list(self, *, page: int, size: int, filters: Optional[Mapping[str, Any]], sort: Optional[List[str]]) -> Dict[str, Any]:
        ctx = get_current_context()
        tenant_id = getattr(ctx, "tenant_id", None)

        where = ["(tenant_id IS NULL OR tenant_id=:tenant_id)"]
        params: Dict[str, Any] = {"tenant_id": tenant_id}

        if filters:
            for k, v in filters.items():
                if k in {"status", "priority"} and v is not None:
                    where.append(f"{k} = :f_{k}")
                    params[f"f_{k}"] = v

        where_sql = " AND ".join(where) if where else "1=1"

        order_sql = "updated_at DESC"
        if sort:
            parts = []
            for s in sort:
                s = s.strip()
                if not s:
                    continue
                desc = s.startswith("-")
                col = s[1:] if desc else s
                if col in COLUMNS:
                    parts.append(f"{col} {'DESC' if desc else 'ASC'}")
            if parts:
                order_sql = ", ".join(parts)

        # total
        eng = get_engine()
        sql_count = f"SELECT COUNT(*) FROM {self.TABLE} WHERE {where_sql}"
        sql2, p2 = adapt_params_for_engine(eng, sql_count, params)
        row = eng.fetchone(sql2) if p2 is None else eng.fetchone(sql2, p2)
        total = int(row[0]) if row else 0

        # items
        offset = (page - 1) * size
        sql_rows = f"SELECT {', '.join(COLUMNS)} FROM {self.TABLE} WHERE {where_sql} ORDER BY {order_sql} LIMIT :limit OFFSET :offset"
        params_rows = dict(params, limit=size, offset=offset)
        items = self._fetchall(sql_rows, params_rows)
        return {"items": items, "total": total, "page": page, "size": size}

    def update(self, entity_id_or_row: Any, patch: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        if patch is None and isinstance(entity_id_or_row, Mapping):
            merged = dict(entity_id_or_row)
            entity_id = str(merged["id"])
        else:
            entity_id = str(entity_id_or_row)
            current = self.get(entity_id)
            if not current:
                raise KeyError("Not found")
            merged = dict(current)
            for k, v in (patch or {}).items():
                if k in {"name","status","description","start_date","due_date","priority","tags","meta","owner_id"}:
                    merged[k] = v

        merged["updated_at"] = now_sql()
        merged["tags"] = dumps_json(merged.get("tags"))
        merged["meta"] = dumps_json(merged.get("meta"))

        ctx = get_current_context()
        tenant_id = getattr(ctx, "tenant_id", None)

        set_cols = [c for c in COLUMNS if c not in ("id","created_at")]
        sets = ", ".join([f"{c}=:{c}" for c in set_cols])
        sql = f"UPDATE {self.TABLE} SET {sets} WHERE id=:id AND (tenant_id IS NULL OR tenant_id=:tenant_id)"
        params = {c: merged.get(c) for c in set_cols}
        params["id"] = entity_id
        params["tenant_id"] = tenant_id
        self._exec(sql, params)
        return self.get(entity_id) or merged

    def delete(self, entity_id: str) -> bool:
        ctx = get_current_context()
        tenant_id = getattr(ctx, "tenant_id", None)
        sql = f"DELETE FROM {self.TABLE} WHERE id=:id AND (tenant_id IS NULL OR tenant_id=:tenant_id)"
        self._exec(sql, {"id": entity_id, "tenant_id": tenant_id})
        return True

    def transition(self, entity_id: str, to_status: Optional[str]) -> Dict[str, Any]:
        current = self.get(entity_id)
        if not current:
            raise KeyError("Not found")
        src = (current.get("status") or "new").strip().lower()
        dst = (to_status or "").strip().lower()
        if not can_transition(src, dst):
            raise ValueError("Invalid transition")
        current["status"] = dst
        return self.update(current)
