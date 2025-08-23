# prefiq/database/health.py

from __future__ import annotations
import asyncio
import inspect
from typing import Any, Optional

async def _maybe_await(x: Any) -> Any:
    """Await x if it is awaitable, otherwise return x."""
    if inspect.isawaitable(x):
        return await x
    return x

async def is_healthy_async(engine: Any, timeout: Optional[float] = 3.0) -> bool:
    """
    Async-safe health check. Works for both sync and async engines.
    If engine.test_connection() is sync, we just call it.
    If it's async, we await it (with an optional timeout).
    """
    try:
        result = engine.test_connection()
        if timeout is not None and timeout > 0:
            return bool(await asyncio.wait_for(_maybe_await(result), timeout=timeout))
        return bool(await _maybe_await(result))
    except Exception:
        return False

def is_healthy(engine: Any, timeout: Optional[float] = 3.0) -> bool:
    """
    Sync entrypoint for health checks, usable from CLIs.
    - If engine.test_connection() is sync → call directly.
    - If it's async → run an event loop just for this probe.
    NOTE: If a loop is already running in this thread, we avoid blocking it
    and simply schedule the check on that loop via a background task and
    return False if we cannot obtain a result synchronously.
    """
    try:
        res = engine.test_connection()
        if not inspect.isawaitable(res):
            return bool(res)
        # No running loop? Safe to run our own.
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(is_healthy_async(engine, timeout))
        # A loop IS running in this thread; we cannot block it here.
        # Best effort: schedule and fail fast to keep this function synchronous.
        asyncio.create_task(is_healthy_async(engine, timeout))
        return False
    except Exception:
        return False
