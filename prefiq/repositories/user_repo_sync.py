from __future__ import annotations
from typing import Optional, Sequence

from prefiq.repositories.base import SupportsSyncDB
from prefiq.repositories.models import User

class UserRepoSync:
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR(255) NOT NULL,
        is_active TINYINT(1) NOT NULL DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    def __init__(self, db: SupportsSyncDB):
        self.db = db

    def migrate(self) -> None:
        self.db.execute(self.CREATE_TABLE_SQL)

    def create(self, user: User) -> int:
        self.db.execute("INSERT INTO users (email, name, is_active) VALUES (%s, %s, %s)",
                        (user.email, user.name, int(user.is_active)))
        row = self.db.fetchone("SELECT LAST_INSERT_ID()")
        return int(row[0]) if row else 0

    def get_by_id(self, user_id: int) -> Optional[User]:
        row = self.db.fetchone("SELECT id, email, name, is_active FROM users WHERE id = %s LIMIT 1",
                               (user_id,))
        if not row:
            return None
        return User(id=row[0], email=row[1], name=row[2], is_active=bool(row[3]))

    def get_by_email(self, email: str) -> Optional[User]:
        row = self.db.fetchone("SELECT id, email, name, is_active FROM users WHERE email = %s LIMIT 1",
                               (email,))
        if not row:
            return None
        return User(id=row[0], email=row[1], name=row[2], is_active=bool(row[3]))

    def list_active(self, limit: int = 100) -> list[User]:
        rows = self.db.fetchall("SELECT id, email, name, is_active FROM users WHERE is_active=1 ORDER BY id DESC LIMIT %s",
                                (limit,))
        return [User(id=r[0], email=r[1], name=r[2], is_active=bool(r[3])) for r in rows]

    def deactivate(self, user_id: int) -> None:
        self.db.execute("UPDATE users SET is_active = 0 WHERE id = %s", (user_id,))

    def bulk_create(self, users: Sequence[User]) -> None:
        params = [(u.email, u.name, int(u.is_active)) for u in users]
        self.db.executemany("INSERT INTO users (email, name, is_active) VALUES (%s, %s, %s)", params)

    def create_with_audit(self, user: User) -> int:
        """
        Multi-statement atomic op using the sync engine's transaction() context.
        """
        with self.db.transaction() as cur:
            cur.execute("INSERT INTO users (email, name, is_active) VALUES (%s, %s, %s)",
                        (user.email, user.name, int(user.is_active)))
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchone()
            new_id = int(row[0]) if row else 0
            cur.execute("INSERT INTO audit_log (entity, entity_id, action) VALUES (%s, %s, %s)",
                        ("user", new_id, "create"))
            return new_id
