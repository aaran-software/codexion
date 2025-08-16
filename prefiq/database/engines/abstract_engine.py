# =============================================================
# Abstract DB Engine Interface (abstract_engine.py)
# file path: prefiq/database/engines/abstract_engine.py
#
# Author: Sundar
# Created: 2025-08-06
#
# Purpose:
#   - Define a unified abstract base class for all database engines.
#   - Standardize lifecycle methods and execution behavior.
#   - Provide built-in support for pre-/post-execution hooks.
#
# Notes for Developers:
#   - All concrete engines (sync/async) must inherit and implement these methods.
#   - Hooks can be used for logging, metrics, or debugging.
# =============================================================

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Sequence, TypeVar, Generic

T = TypeVar('T')  # NEW: Generic type for query results

# Type alias for query hooks: function(query, params, stage)
HookType = Optional[Callable[[str, Optional[tuple], str], None]]


class AbstractEngine(ABC, Generic[T]):
    """
    Abstract base class for all database engine implementations.
    Includes hook support and method declarations for full DB lifecycle.
    """

    def __init__(self):
        self.before_execute_hook: HookType = None
        self.after_execute_hook: HookType = None

    def set_before_execute_hook(self, hook_func: HookType) -> None:
        """Register a function to be called before executing any query."""
        self.before_execute_hook = hook_func

    def set_after_execute_hook(self, hook_func: HookType) -> None:
        """Register a function to be called after executing any query."""
        self.after_execute_hook = hook_func

    def _run_hooks(self, stage: str, query: str, params: Optional[tuple] = None) -> None:
        """
        Run registered hooks (if any) for a given stage.

        :param stage: 'before' or 'after'
        :param query: SQL query string
        :param params: Optional query parameters
        """
        hook = self.before_execute_hook if stage == 'before' else self.after_execute_hook
        if hook:
            hook(query, params, stage)

    @abstractmethod
    def connect(self) -> None:
        """Establish a database connection."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Close the active database connection."""
        ...

    @abstractmethod
    def execute(self, query: str, params: Optional[tuple] = None) -> None:
        """Execute a write operation (INSERT, UPDATE, DELETE)."""
        ...

    @abstractmethod
    def fetchone(self, query: str, params: Optional[tuple] = None) -> Optional[T]:
        """Execute a SELECT query and return a single result."""
        ...

    @abstractmethod
    def fetchall(self, query: str, params: Optional[tuple] = None) -> list[T]:
        """Execute a SELECT query and return all results."""
        ...

    @abstractmethod
    def executemany(self, query: str, param_list: Sequence[tuple]) -> None:
        """Execute a bulk write operation with multiple param sets."""
        ...

    @abstractmethod
    def begin(self) -> None:
        """Begin a new transaction (if supported)."""
        ...

    @abstractmethod
    def commit(self) -> None:
        """Commit the current transaction."""
        ...

    @abstractmethod
    def rollback(self) -> None:
        """Rollback the current transaction."""
        ...

    @abstractmethod
    def test_connection(self) -> bool:
        """Check if the connection to the database is alive."""
        ...
