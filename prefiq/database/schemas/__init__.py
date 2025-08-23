from __future__ import annotations
# Re-export the shims so `from prefiq.database.schemas import blueprint, builder, queries` works.
from . import blueprint, builder, queries  # type: ignore

__all__ = ["blueprint", "builder", "queries"]
