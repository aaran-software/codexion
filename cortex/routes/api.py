# apps/blog/routes/api.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/posts" , tags=["blog:api"])
def list_posts():
    return [{"id": 1, "title": "hello"}]
