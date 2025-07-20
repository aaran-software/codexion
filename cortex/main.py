# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cortex.routes import api
from cortex.core.config import get_settings

app = FastAPI(
    title="Codexion API",
    version="1.0.0",
    description="Welcome to the Codexion Backend"
)
settings = get_settings()

app.include_router(api.router, prefix="/api")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# print(get_settings().DATABASE_URL)

@app.get("/")
async def root():
    return {"message": "Welcome to Codexion API"}

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=4000,
        reload=True
    )