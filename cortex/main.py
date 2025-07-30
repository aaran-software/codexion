# app/main.py

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure .env exists before loading settings
from cortex.core.startup import ensure_env_file
ensure_env_file()

from cortex.core.settings import get_settings
from cortex.DTO.dal import engine, Base
import cortex.models.user
from cortex.routes import api

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title="Codexion API",
    version="1.0.0",
    description="Welcome to the Codexion Backend"
)

settings = get_settings()

app.include_router(api.router, prefix="/api")

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

@app.get("/")
async def root():
    return {"message": "Welcome to sundar Codexion API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=4001, reload=True)
