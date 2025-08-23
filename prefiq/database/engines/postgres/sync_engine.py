from __future__ import annotations

from typing import Any, Optional, Sequence, Tuple

# Reuse the async engine under the hood and provide a sync-looking API.
# This keeps the placeholder style ($1) consistent with our PostgresDialect.
from .async_engine import AsyncPostgresEngine


class SyncPostgresEngine(AsyncPostgresEngine):
    """
    Sync facade backed by AsyncPostgresEngine.
    Public methods are the same: execute(), fetchone(), fetchall(), close().
    """

    driver = "asyncpg(sync-wrapper)"  # for diagnostics

    # All behavior is inherited; the asyncpg-backed _run() provides blocking calls.
    # If later you prefer psycopg (true sync), swap the parent implementation accordingly.
