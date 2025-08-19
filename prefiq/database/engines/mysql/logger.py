# prefiq/database/engines/mysql/logger.py

from __future__ import annotations

import time
from prefiq.settings.get_settings import load_settings
from prefiq.log.logger import get_logger

# Load app settings / namespace
_s = load_settings()
_log = get_logger(f"{_s.LOG_NAMESPACE}.db.query")

# Slow threshold in milliseconds.
# You can expose this via settings later (e.g., _s.DB_SLOW_MS_SQLITE or env).
_SLOW_MS = 500


def log_query(query: str, start_time: float) -> None:
    """
    Emit a structured log for a completed SQL query with elapsed time.
    - INFO for normal queries
    - WARNING for slow queries (>= _SLOW_MS)
    """
    elapsed_ms = int((time.time() - start_time) * 1000)
    payload = {"elapsed_ms": elapsed_ms, "query": query}

    if elapsed_ms >= _SLOW_MS:
        _log.warning("query_slow", extra=payload)
    else:
        _log.info("query_ok", extra=payload)
