# apps/blog/src/routes/api.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/posts")
def list_posts():
    return [{"id": 1, "title": "hello"}]
