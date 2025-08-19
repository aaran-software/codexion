# prefiq/database/engines/mysql/hooks.py

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
