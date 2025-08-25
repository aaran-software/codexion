# apps/blog/src/routes/web.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/blog", tags=["blog:web"])
def homepage():
    return {"page": "blog home"}
