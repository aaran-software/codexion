# prefiq/database/hooks.py

from typing import Optional, Any
from prefiq.log.logger import get_logger

log = get_logger("prefiq.db")

def before_execute(query: str, params: Optional[tuple] = None, stage: str = "before") -> None:
    try:
        log.debug("db_before_execute", extra={"query": query, "params": params})
    except Exception:
        pass

def after_execute(query: str, params: Optional[tuple] = None, stage: str = "after") -> None:
    try:
        log.debug("db_after_execute", extra={"query": query, "params": params})
    except Exception:
        pass
