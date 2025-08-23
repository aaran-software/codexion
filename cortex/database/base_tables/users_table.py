# cortex/database/migration/tenants.py

from prefiq.database.migrations.base import Migrations

class User(Migrations):
    APP_NAME    = "cortex"
    TABLE_NAME  = "Users"
    ORDER_INDEX = 0

    def up(self) -> None:
        self.create("Users", lambda t: [
            t.id(),
            t.string("name"),
            t.string("email").unique(),
            t.string("password_hash"),
            t.timestamps(),
        ])

    def down(self) -> None:
        self.drop_if_exists("Users")