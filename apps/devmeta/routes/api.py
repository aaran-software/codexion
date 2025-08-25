# apps/blog/src/routes/api.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/devmeta" , tags=["blog:api"])
def list_posts():
    return [{"id": 1, "title": "devmeta"}]
