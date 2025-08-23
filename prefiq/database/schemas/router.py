from __future__ import annotations
from typing import Literal

from prefiq.database.dialects.registry import get_dialect

Driver = Literal["mysql_like", "sqlite", "postgres"]

def current_driver() -> Driver:
    d = get_dialect()
    name = d.name() if callable(getattr(d, "name", None)) else getattr(d, "name", "")
    n = (name or "").lower()
    if "mariadb" in n or "mysql" in n:
        return "mysql_like"
    if "postgres" in n:
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
