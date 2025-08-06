from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Sequence

HookType = Optional[Callable[[str, Optional[tuple], str], None]]

class AbstractEngine(ABC):
    def __init__(self):
        self.before_execute_hook: HookType = None
        self.after_execute_hook: HookType = None

    def set_before_execute_hook(self, hook_func: HookType) -> None:
        self.before_execute_hook = hook_func

    def set_after_execute_hook(self, hook_func: HookType) -> None:
        self.after_execute_hook = hook_func

    def _run_hooks(self, stage: str, query: str, params: Optional[tuple] = None) -> None:
        hook = self.before_execute_hook if stage == 'before' else self.after_execute_hook
        if hook:
            hook(query, params, stage)

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def execute(self, query: str, params: Optional[tuple] = None) -> None: ...

    @abstractmethod
    def fetchone(self, query: str, params: Optional[tuple] = None) -> Any: ...

    @abstractmethod
    def fetchall(self, query: str, params: Optional[tuple] = None) -> list[Any]: ...

    @abstractmethod
    def executemany(self, query: str, param_list: Sequence[tuple]) -> None: ...

    @abstractmethod
    def begin(self) -> None: ...

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...

    @abstractmethod
    def test_connection(self) -> bool: ...