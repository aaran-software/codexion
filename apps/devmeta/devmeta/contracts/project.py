# =============================================
# app/contracts/project.py
# =============================================
from typing import Protocol

class IProject(Protocol):
    id: Optional[int]
    name: str
    slug: str
    meta: Dict[str, Any]
