# apps/devmeta/core/services/project_service.py
# =============================================

from __future__ import annotations

from typing import Any, Dict
from apps.devmeta.core.models.project import Project
from apps.devmeta.core.repositories.project_repository import ProjectRepository
from prefiq.abstracts.service import AService


class ProjectService(AService[Project]):
    repository: ProjectRepository

    def __init__(self, repository: ProjectRepository):
        self.repository = repository
        super().__init__(repository=repository)

    def before_create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        slug = data.get("slug") or data.get("name", "").strip().lower().replace(" ", "-")
        data["slug"] = slug
        data.setdefault("meta", {})
        return data
