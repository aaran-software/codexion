from __future__ import annotations

from dataclasses import dataclass, asdict
from math import ceil
from typing import Generic, TypeVar, Iterable, Dict, Any

T = TypeVar("T")

@dataclass
class Page:
    number: int = 1
    size: int = 20

    def offset(self) -> int:
        return max(0, (max(1, self.number) - 1) * max(1, self.size))

@dataclass
class PagedResult(Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int

    @property
    def pages(self) -> int:
        return ceil(self.total / self.size) if self.size > 0 else 1

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    def to_dict(self) -> Dict[str, Any]:
        return {
            "items": self.items,
            "total": self.total,
            "page": self.page,
            "size": self.size,
            "pages": self.pages,
            "has_next": self.has_next,
        }
