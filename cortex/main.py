# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cortex.routes import api
from cortex.core.config import get_settings

app = FastAPI()

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

print(get_settings().DATABASE_URL)