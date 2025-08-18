# =============================================================
# Query Logger (logger.py)
#
# Author: Sundar
# Created: 2025-08-06
#
# Purpose:
#   - Log SQL query execution time.
#   - Flag slow queries for diagnostics.
#
# Notes for Developers:
#   - Default threshold is 1s; adjust `SLOW_QUERY_THRESHOLD` if needed.
#   - This logger prints to stdout; replace with structured logger if needed.
# =============================================================

import time
from prefiq.settings.get_settings import load_settings
from prefiq.utils.logger import get_logger

_s = load_settings()
_log = get_logger(f"{_s.LOG_NAMESPACE}.db.query")

# slow threshold in ms (optional; add to settings if you like)
_SLOW_MS = 500

def log_query(query: str, start_time: float) -> None:
    elapsed_ms = int((time.time() - start_time) * 1000)
    extra = {"elapsed_ms": elapsed_ms}
    if elapsed_ms >= _SLOW_MS:
        _log.warning("query_slow", extra={**extra, "query": query})
    else:
        _log.info("query_ok", extra={**extra, "query": query})
