# =============================================================
# Retry Logic (retry.py)
#
# Author: ChatGPT
# Created: 2025-08-06
#
# Purpose:
#   - Provide automatic retry mechanism for transient DB operations.
#   - Handles common recoverable exceptions like connection errors.
#
# Notes for Developers:
#   - Can be used with both sync and async engines.
#   - Accepts optional `retries`, `delay`, and `backoff` parameters.
# =============================================================

import asyncio
import time
import mariadb
from typing import Callable, TypeVar, Awaitable

from mariadb import Error

T = TypeVar("T")


def with_retry(
        func: Callable[[], T],
        retries: int = 3,
        delay: float = 0.2,
        backoff: float = 2.0,
) -> T:
    """
    Retry a synchronous function with exponential backoff.

    :param func: Function to execute
    :param retries: Max number of retries
    :param delay: Initial delay between retries (in seconds)
    :param backoff: Backoff multiplier (e.g., 2.0 doubles delay each time)
    :return: The function's return value if successful
    :raises: The last exception raised if all retries fail
    """
    for attempt in range(retries):
        e: Error
        try:
            return func()
        except mariadb.Error:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
            delay *= backoff
    return None


async def with_retry_async(
        func: Callable[[], Awaitable[T]],
        retries: int = 3,
        delay: float = 0.2,
        backoff: float = 2.0,
) -> T:
    """
    Retry an async function with exponential backoff.

    :param func: Async function to execute
    :param retries: Max number of retries
    :param delay: Initial delay between retries (in seconds)
    :param backoff: Backoff multiplier (e.g., 2.0 doubles delay each time)
    :return: The function's result if successful
    :raises: The last exception raised if all retries fail
    """
    for attempt in range(retries):
        try:
            return await func()
        except mariadb.Error:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(delay)
            delay *= backoff
    return None
