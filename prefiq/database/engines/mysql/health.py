# prefiq/database/engines/mysql/health.py

from __future__ import annotations
import asyncio
import inspect
from typing import Any, Optional

async def _awaitable(x: Any) -> Any:
    if inspect.iscoroutine(x):
        return await x
    return x  # sync value

async def _is_healthy_async(engine, timeout: Optional[float]) -> bool:
    try:
        res = engine.test_connection()
        if timeout is not None:
            res = await asyncio.wait_for(_awaitable(res), timeout=timeout)
        else:
            res = await _awaitable(res)
        return bool(res)
    except (ValueError, TypeError):
        return False

def is_healthy(engine, timeout: Optional[float] = 3.0) -> bool:
    """
    True if engine.test_connection() succeeds; supports sync/async engines.

    timeout: seconds for async engines (None = no timeout).
    """
    # If we're already in an event loop, do it fully async.
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Caller is async; schedule as a task and let them await it if they want.
        # For convenience, run-to-completion here (small, self-contained probe).
        return loop.run_until_complete(_is_healthy_async(engine, timeout))  # type: ignore[call-arg]

    # No loop → run an event loop if needed
    try:
        res = engine.test_connection()
        if inspect.isawaitable(res):
            return asyncio.run(_is_healthy_async(engine, timeout))
        return bool(res)
    except (ValueError, TypeError):
        return False
