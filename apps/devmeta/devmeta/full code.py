# =============================================
# Project Skeleton
# =============================================
# Suggested folders (create these in your repo):
#
# core/
#   contracts/
#     controller.py
#     model.py
#     repository.py
#     service.py
#   abstracts/
#     controller.py
#     model.py
#     repository.py
#     service.py
# app/
#   contracts/
#     project.py
#   models/
#     project.py
#   repositories/
#     project_repository.py
#   services/
#     project_service.py
#   controllers/
#     project_rest_controller.py
# routing/
#   api.py
#   web.py
# main.py
# =============================================























# wiring happens in main.py after dependencies are created



# =============================================
# main.py
# =============================================
from fastapi import FastAPI

# Instantiate core components and wire dependencies
project_repo = ProjectRepository()
project_service = ProjectService(project_repo)
project_controller = ProjectRestController(project_service)

app = FastAPI(title="Prefiq API")

# include routers
from routing.api import api_router
from routing.web import web_router

api_router.include_router(project_controller.router)
app.include_router(api_router)
app.include_router(web_router)

# Run with: uvicorn main:app --reload
