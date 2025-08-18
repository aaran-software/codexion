from __future__ import annotations
from typing import Optional, Sequence, Any

from prefiq.repositories.base import SupportsAsyncDB
from prefiq.repositories.models import User
from prefiq.database.engines.mariadb.pool import _run_in_thread  # for cursor ops inside tx (if needed)

class UserRepoAsync:
    """
    Async repository for users table.
    Assumes MariaDB and a simple schema as below.
    """

    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR(255) NOT NULL,
        is_active TINYINT(1) NOT NULL DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    def __init__(self, db: SupportsAsyncDB):
        self.db = db

    async def migrate(self) -> None:
        await self.db.execute(self.CREATE_TABLE_SQL)

    async def create(self, user: User) -> int:
        sql = "INSERT INTO users (email, name, is_active) VALUES (%s, %s, %s)"
        await self.db.execute(sql, (user.email, user.name, int(user.is_active)))
        # MariaDB: fetch last insert id
        row = await self.db.fetchone("SELECT LAST_INSERT_ID()")
        return int(row[0]) if row else 0

    async def get_by_id(self, user_id: int) -> Optional[User]:
        row = await self.db.fetchone(
            "SELECT id, email, name, is_active FROM users WHERE id = %s LIMIT 1",
            (user_id,),
        )
        if not row:
            return None
        return User(id=row[0], email=row[1], name=row[2], is_active=bool(row[3]))

    async def get_by_email(self, email: str) -> Optional[User]:
        row = await self.db.fetchone(
            "SELECT id, email, name, is_active FROM users WHERE email = %s LIMIT 1",
            (email,),
        )
        if not row:
            return None
        return User(id=row[0], email=row[1], name=row[2], is_active=bool(row[3]))

    async def list_active(self, limit: int = 100) -> list[User]:
        rows = await self.db.fetchall(
            "SELECT id, email, name, is_active FROM users WHERE is_active = 1 ORDER BY id DESC LIMIT %s",
            (limit,),
        )
        return [User(id=r[0], email=r[1], name=r[2], is_active=bool(r[3])) for r in rows]

    async def deactivate(self, user_id: int) -> None:
        await self.db.execute("UPDATE users SET is_active = 0 WHERE id = %s", (user_id,))

    async def bulk_create(self, users: Sequence[User]) -> None:
        sql = "INSERT INTO users (email, name, is_active) VALUES (%s, %s, %s)"
        params = [(u.email, u.name, int(u.is_active)) for u in users]
        await self.db.executemany(sql, params)

    async def create_with_audit(self, user: User) -> int:
        """
        Example of multi-statement atomic op using transaction().
        Requires AsyncMariaDBEngine.transaction context.
        """
        async with self.db.transaction() as cur:
            # cur is a real MariaDB cursor (blocking) → use _run_in_thread for its methods
            await _run_in_thread(cur.execute, "INSERT INTO users (email, name, is_active) VALUES (%s, %s, %s)",
                                 user.email, user.name, int(user.is_active))
            # get id
            await _run_in_thread(cur.execute, "SELECT LAST_INSERT_ID()")
            row = await _run_in_thread(cur.fetchone)
            new_id = int(row[0]) if row else 0
            # audit row (simple example)
            await _run_in_thread(cur.execute, "INSERT INTO audit_log (entity, entity_id, action) VALUES (%s, %s, %s)",
                                 "user", new_id, "create")
            return new_id
