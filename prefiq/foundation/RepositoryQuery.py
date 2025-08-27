from __future__ import annotations

from typing import Any, Dict, Mapping, Generic, TypeVar, Sequence

from prefiq.contracts.IDomain import IDomain
from prefiq.foundation.Mapper import Mapper
from prefiq.foundation.Pagination import PagedResult

T = TypeVar("T", bound=IDomain)

class SqlDriver:
    """
    Minimal driver surface we rely on.
    Substitute with your real engine (e.g., your existing get_engine()).
    """
    def execute(self, sql: str, params: Mapping[str, Any] | None = None) -> Sequence[Dict[str, Any]]:
        raise NotImplementedError

class SqlRepository(Generic[T]):
    """
    Portable SQL repository using a very small driver interface.
    Expects a table with a `tenant_id` column for isolation.
    """

    def __init__(self, table: str, mapper: Mapper[T], driver: SqlDriver) -> None:
        self.table = table
        self.mapper = mapper
        self.driver = driver

    # NOTE: sql here is intentionally simple; adapt to your dialect as needed.
    def create(self, entity: T) -> Dict[str, Any]:
        rec = self.mapper.to_record(entity)
        cols = ", ".join(rec.keys())
        ph = ", ".join(f":{k}" for k in rec.keys())
        self.driver.execute(f"INSERT INTO {self.table} ({cols}) VALUES ({ph})", rec)
        return rec

    def get(self, tenant_id: str | None, entity_id: str) -> Dict[str, Any] | None:
        rows = self.driver.execute(
            f"SELECT * FROM {self.table} WHERE id = :id AND tenant_id IS :tid OR tenant_id = :tid",
            {"id": entity_id, "tid": tenant_id},
        )
        return rows[0] if rows else None

    def update(self, entity: T) -> Dict[str, Any]:
        rec = self.mapper.to_record(entity)
        assigns = ", ".join(f"{k} = :{k}" for k in rec.keys() if k not in ("id",))
        self.driver.execute(
            f"UPDATE {self.table} SET {assigns} WHERE id = :id AND (tenant_id IS :tid OR tenant_id = :tid)",
            rec | {"tid": rec.get("tenant_id")},
        )
        return rec

    def delete(self, tenant_id: str | None, entity_id: str) -> bool:
        rows = self.driver.execute(
            f"DELETE FROM {self.table} WHERE id = :id AND (tenant_id IS :tid OR tenant_id = :tid) RETURNING id",
            {"id": entity_id, "tid": tenant_id},
        )
        return bool(rows)

    def list(
        self,
        tenant_id: str | None,
        page: int,
        size: int,
        filters: Mapping[str, Any] | None,
        sort: list[str] | None,
    ) -> PagedResult[Dict[str, Any]]:
        where = ["(tenant_id IS :tid OR tenant_id = :tid)"]
        params: Dict[str, Any] = {"tid": tenant_id}
        if filters:
            for i, (k, v) in enumerate(filters.items()):
                where.append(f"{k} = :f{i}")
                params[f"f{i}"] = v
        order = ""
        if sort:
            order = " ORDER BY " + ", ".join(f"{s[1:]} DESC" if s.startswith("-") else f"{s} ASC" for s in sort)
        count_rows = self.driver.execute(
            f"SELECT COUNT(*) AS c FROM {self.table} WHERE " + " AND ".join(where),
            params,
        )
        total = int(count_rows[0]["c"]) if count_rows else 0
        offset = max(0, (max(1, page) - 1) * max(1, size))
        rows = self.driver.execute(
            f"SELECT * FROM {self.table} WHERE " + " AND ".join(where) + order + " LIMIT :lim OFFSET :off",
            params | {"lim": size, "off": offset},
        )
        return PagedResult(items=list(rows), total=total, page=page, size=size)
