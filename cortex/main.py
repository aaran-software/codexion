# app/main.py

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import engine and Base from your single source of truth
from cortex.DTO.dal import engine, Base
# Import your models so they register with Base.metadata
import cortex.models.user

from cortex.routes import api
from cortex.core.config import get_settings

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
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Now Base is defined
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to Codexion API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=4000, reload=True)

    for route in app.routes:
        print(route.path)
