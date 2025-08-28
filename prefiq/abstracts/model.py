# prefiq/abstracts/model.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

__all__ = ["AModel"]


class AModel(ABC):
    """Base entity contract for in-memory/DB-backed models."""

    id: Optional[int] = None

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AModel":
        raise NotImplementedError
