# prefiq/database/migrations/discover.py
from prefiq.database.migrations.base import Migrations

def discover_all() -> list[type[Migrations]]:
    # subclasses of Migrations across imports
    # ensure all migration modules are imported before calling
    return sorted(Migrations.__subclasses__(), key=lambda c: c.ORDER_INDEX)
