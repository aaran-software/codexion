# prefiq/database/schemas/router.py
from __future__ import annotations
from typing import Literal
from prefiq.settings.get_settings import load_settings

Driver = Literal["mysql_like", "sqlite", "postgres"]

def current_driver() -> Driver:
    eng = (load_settings().DB_ENGINE or "").strip().lower()
    if eng in ("mariadb", "mysql"):
        return "mysql_like"
    if eng in ("postgres", "postgresql", "pg"):
        return "postgres"
    return "sqlite"

def impl():
    drv = current_driver()
    if drv == "mysql_like":
        from prefiq.database.schemas.mysql_like import blueprint, builder, queries
        return blueprint, builder, queries
    if drv == "postgres":
        from prefiq.database.schemas.postgres import blueprint, builder, queries
        return blueprint, builder, queries
    from prefiq.database.schemas.sqlite import blueprint, builder, queries
    return blueprint, builder, queries
