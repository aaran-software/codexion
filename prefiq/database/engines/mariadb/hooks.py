# =============================================================
# Query Hooks (hooks.py)
#
# Author: Sundar
# Created: 2025-08-06
#
# Purpose:
#   - Provide default before/after execution hooks for DB queries.
#   - Useful for logging, auditing, or injecting instrumentation.
#
# Notes for Developers:
#   - Can be overridden by setting `set_before_execute_hook()` or `set_after_execute_hook()`
#   - Hook functions receive `query`, `params`, and `stage` (either 'before' or 'after')
# =============================================================

from typing import Optional


def default_before_hook(query: str, params: Optional[tuple], stage: str) -> None:
    """
    Default hook called before executing a query.

    :param query: SQL query string
    :param params: Query parameters tuple (if any)
    :param stage: Execution stage ('before')
    """
    print(f"[HOOK] {stage.upper()} QUERY: {query} PARAMS: {params}")


def default_after_hook(query: str, params: Optional[tuple], stage: str) -> None:
    """
    Default hook called after executing a query.

    :param query: SQL query string
    :param params: Query parameters tuple (if any)
    :param stage: Execution stage ('after')
    """
    print(f"[HOOK] {stage.upper()} QUERY COMPLETE")
