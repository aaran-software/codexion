# cortex/database/migrations/tenants.py

from prefiq.database.migrations.base import Migrations

class Tenants(Migrations):
    APP_NAME    = "cortex"
    TABLE_NAME  = "tenants"
    ORDER_INDEX = 1

    def up(self) -> None:
        self.create("tenants", lambda t: [
            t.id(),
            t.string("name"),
            t.timestamps(),
        ])

    def down(self) -> None:
        self.drop_if_exists("tenants")