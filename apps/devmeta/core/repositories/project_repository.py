# apps/devmeta/core/repositories/project_repository.py
# =============================================
from typing import Any, Dict

from apps.devmeta.core.models.project import Project
from prefiq.abstracts.repository import ARepository


class ProjectRepository(ARepository[Project]):
    def _build(self, data: Dict[str, Any]) -> Project:
        return Project.from_dict(data)