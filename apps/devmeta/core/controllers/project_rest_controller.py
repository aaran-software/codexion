# apps/devmeta/core/controllers/project_rest_controller.py
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from apps.devmeta.core.services.project_service import ProjectService

# Pydantic I/O schemas
class ProjectIn(BaseModel):
    name: str
    slug: Optional[str] = None
    meta: Dict[str, Any] | None = None

class ProjectOut(BaseModel):
    id: int
    name: str
    slug: str
    meta: Dict[str, Any]

class ProjectRestController:
    def __init__(self, service: ProjectService):
        self.service = service
        self.router = APIRouter(prefix="/projects", tags=["projects"])
        self._register()

    def _register(self) -> None:
        @self.router.get("/", response_model=Dict[str, Any])
        def index(page: int = 1, per_page: int = 20):
            return self.service.paginate(page, per_page)

        @self.router.get("/{project_id}", response_model=ProjectOut)
        def show(project_id: int):
            proj = self.service.get(project_id)
            if not proj:
                raise HTTPException(status_code=404, detail="Project not found")
            return ProjectOut(**proj.to_dict())

        @self.router.post("/", response_model=ProjectOut, status_code=201)
        def store(payload: ProjectIn):
            proj = self.service.create(payload.model_dump())
            return ProjectOut(**proj.to_dict())

        @self.router.put("/{project_id}", response_model=ProjectOut)
        def update(project_id: int, payload: ProjectIn):
            updated = self.service.update(project_id, payload.model_dump(exclude_unset=True))
            if not updated:
                raise HTTPException(status_code=404, detail="Project not found")
            return ProjectOut(**updated.to_dict())

        @self.router.delete("/{project_id}", status_code=204)
        def destroy(project_id: int):
            ok = self.service.delete(project_id)
            if not ok:
                raise HTTPException(status_code=404, detail="Project not found")
            return None

# Helper to build controller with DI
def get_project_controller(service: ProjectService = Depends()):
    return ProjectRestController(service)
