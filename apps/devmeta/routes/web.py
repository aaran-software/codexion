# apps/blog/src/routes/web.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/devmeta", tags=["devmeta:web"])
def homepage():
    return {"page": "devmeta home"}
