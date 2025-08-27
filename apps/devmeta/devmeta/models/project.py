# =============================================
# app/models/project.py
# =============================================
from dataclasses import dataclass, field

@dataclass
class Project(AModel):
    name: str
    slug: str
    meta: Dict[str, Any] = field(default_factory=dict)
    id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "slug": self.slug, "meta": self.meta}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        return cls(id=data.get("id"), name=data["name"], slug=data["slug"], meta=data.get("meta", {}))