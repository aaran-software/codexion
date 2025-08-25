# apps/devmeta/routes/api.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/posts", tags=["devmeta:api"])
def list_posts():
    return [{"id": 1, "title": "hello"}]
