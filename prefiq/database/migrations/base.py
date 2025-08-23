# prefiq/database/migrations/base.py
from __future__ import annotations
import re
from typing import Optional

# re-use your builder under the hood
from prefiq.database.schemas.builder import create as _create, drop_if_exists as _drop_if_exists

class Migrations:
    APP_NAME: str = "core"
    TABLE_NAME: Optional[str] = None   # if None, derive from class name → snake_case
    ORDER_INDEX: int = 0

    # ---- convenience helpers (instance methods) ----
    def create(self, *args, **kwargs):
        return _create(*args, **kwargs)

    def drop_if_exists(self, *args, **kwargs):
        return _drop_if_exists(*args, **kwargs)

    # ---- override these (no decorators needed) ----
    def up(self) -> None:
        raise NotImplementedError

    def down(self) -> None:
        pass

    # ---- utility used by the runner ----
    @classmethod
    def derived_table_name(cls) -> str:
        if cls.TABLE_NAME:
            return cls.TABLE_NAME
        # CamelCase → snake_case
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
