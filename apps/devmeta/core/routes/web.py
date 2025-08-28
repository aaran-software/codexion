# apps/devmeta/core/routes/web.py

from fastapi import APIRouter, Depends, HTTPException,  Form
from fastapi.responses import HTMLResponse, RedirectResponse
from apps.devmeta.core.services.project_service import ProjectService
from apps.devmeta.core.repositories.project_repository import ProjectRepository

web_router = APIRouter()

def get_project_service() -> ProjectService:
    return ProjectService(ProjectRepository())

@web_router.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Devmeta</h1><p>Welcome to Project Manager</p>"

@web_router.get("/projects", response_class=HTMLResponse)
def projects_index(service: ProjectService = Depends(get_project_service), page: int = 1, per_page: int = 20):
    data = service.paginate(page, per_page)
    # Simple HTML list (swap to Jinja later)
    items = "".join(f"<li><a href='/projects/{p['id']}'>{p['name']}</a></li>" for p in data['items'])
    return f"<h1>Projects</h1><ul>{items}</ul><a href='/projects/create'>Create Project</a>"

@web_router.get("/projects/create", response_class=HTMLResponse)
def projects_create_form():
    return """
    <h1>Create Project</h1>
    <form method="post" action="/projects">
      <label>Name <input name="name" required /></label><br/>
      <label>Slug <input name="slug" /></label><br/>
      <button type="submit">Save</button>
    </form>
    """

@web_router.post("/projects")
def projects_store(name: str = Form(...), slug: str = Form(None), service: ProjectService = Depends(get_project_service)):
    proj = service.create({"name": name, "slug": slug})
    return RedirectResponse(url=f"/projects/{proj.id}", status_code=303)

@web_router.get("/projects/{project_id}", response_class=HTMLResponse)
def projects_show(project_id: int, service: ProjectService = Depends(get_project_service)):
    proj = service.get(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return f"<h1>{proj.name}</h1><p>Slug: {proj.slug}</p><a href='/projects/{proj.id}/edit'>Edit</a>"

@web_router.get("/projects/{project_id}/edit", response_class=HTMLResponse)
def projects_edit_form(project_id: int, service: ProjectService = Depends(get_project_service)):
    proj = service.get(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return f"""
    <h1>Edit Project</h1>
    <form method="post" action="/projects/{proj.id}/update">
      <label>Name <input name="name" value="{proj.name}" required /></label><br/>
      <label>Slug <input name="slug" value="{proj.slug}" /></label><br/>
      <button type="submit">Update</button>
    </form>
    <form method="post" action="/projects/{proj.id}/delete" style="margin-top:1rem">
      <button type="submit">Delete</button>
    </form>
    """

@web_router.post("/projects/{project_id}/update")
def projects_update(project_id: int, name: str = Form(...), slug: str = Form(None), service: ProjectService = Depends(get_project_service)):
    updated = service.update(project_id, {"name": name, "slug": slug})
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return RedirectResponse(url=f"/projects/{project_id}", status_code=303)

@web_router.post("/projects/{project_id}/delete")
def projects_destroy(project_id: int, service: ProjectService = Depends(get_project_service)):
    ok = service.delete(project_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found")
    return RedirectResponse(url="/projects", status_code=303)
