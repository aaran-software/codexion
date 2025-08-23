# cortex/database/migrations/users_table.py
from prefiq.database.migrations.base import Migrations

class Users(Migrations):
    APP_NAME    = "cortex"
    TABLE_NAME  = "users"     # use lowercase for portability
    ORDER_INDEX = 2           # after tenants

    def up(self) -> None:
        def schema(t):
            return [
                t.id(),
                t.string("name", nullable=False),
                t.string("email", nullable=False, length=320),
                t.string("password_hash", nullable=False, length=255),
                t.timestamps(),
                # table-level constraints / indexes (no chaining)
                t.unique("uq_users_email", ["email"]),
                t.index("idx_users_email", "email"),
            ]
        self.create("users", schema)

    def down(self) -> None:
        self.drop_if_exists("users")
