# app/main.py

import logging
from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from cortex.core.startup import ensure_env_file
ensure_env_file()
from cortex.core.settings import get_settings
from cortex.DTO.dal import engine, Base
import cortex.models.user
from cortex.routes import api
from cortex.core.context import mount_vite, template_context  # ✅ Corrected import order

logging.basicConfig(level=logging.DEBUG)

# ✅ Define FastAPI app first
app = FastAPI(
    title="Codexion API",
    version="1.0.0",
    description="Welcome to the Codexion Backend"
)

# ✅ Now mount Vite build directory after app is defined
mount_vite(app)

settings = get_settings()

app.include_router(api.router, prefix="/api")
for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"{route.path} -> {route.name}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# ✅ Define templates directory
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@app.get("/")
def home(context: dict = Depends(template_context)):
    return templates.TemplateResponse("pages/home.j2", context)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=4001, reload=False)
