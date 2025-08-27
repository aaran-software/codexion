# =============================================
# apps/devmeta/core/contracts/project.py
# =============================================
from typing import Protocol, Optional, Dict, Any


class IProject(Protocol):
    id: Optional[int]
    name: str
    slug: str
    meta: Dict[str, Any]
