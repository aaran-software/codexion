# prefiq/database/schemas/blueprint.py
from __future__ import annotations
from prefiq.database.schemas.router import impl
TableBlueprint = impl()[0].TableBlueprint
__all__ = ["TableBlueprint"]
