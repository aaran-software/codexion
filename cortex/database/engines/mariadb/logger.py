# =============================================================
# Query Logger (logger.py)
#
# Author: ChatGPT
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

SLOW_QUERY_THRESHOLD = 1.0  # seconds

def log_query(query: str, start_time: float):
    """
    Log the duration of a SQL query and flag slow queries.

    :param query: The SQL query string
    :param start_time: The start time (from time.time())
    """
    duration = time.time() - start_time
    if duration > SLOW_QUERY_THRESHOLD:
        print(f"🐢 SLOW QUERY ({duration:.2f}s): {query}")
    else:
        print(f"✅ Query executed in {duration:.2f}s: {query}")