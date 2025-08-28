# apps/devmeta/core/routes/api.py
from fastapi import APIRouter, Depends
from apps.devmeta.core.controllers.project_rest_controller import ProjectRestController
from apps.devmeta.core.services.project_service import ProjectService
from apps.devmeta.core.repositories.project_repository import ProjectRepository

api_router = APIRouter(prefix="/api")

# Very light DI wiring
def get_project_service() -> ProjectService:
    return ProjectService(ProjectRepository())

project_controller = ProjectRestController(service=get_project_service())
api_router.include_router(project_controller.router)
