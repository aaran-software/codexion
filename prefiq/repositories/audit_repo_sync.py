from __future__ import annotations
from typing import Optional, Any

from prefiq.repositories.base import SupportsSyncDB

class AuditRepoSync:
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS audit_log(
      id BIGINT AUTO_INCREMENT PRIMARY KEY,
      entity VARCHAR(100) NOT NULL,
      entity_id BIGINT NOT NULL,
      action VARCHAR(100) NOT NULL,
      meta JSON NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    def __init__(self, db: SupportsSyncDB):
        self.db = db

    def migrate(self) -> None:
        self.db.execute(self.CREATE_TABLE_SQL)

    def log(self, entity: str, entity_id: int, action: str, meta: Optional[dict[str, Any]] = None) -> None:
        self.db.execute(
            "INSERT INTO audit_log(entity, entity_id, action, meta) VALUES (%s, %s, %s, %s)",
            (entity, entity_id, action, (None if meta is None else str(meta)))
        )
