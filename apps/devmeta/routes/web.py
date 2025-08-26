# apps/devmeta/routes/web.py
from fastapi import APIRouter

router = APIRouter()

@router.get("", tags=["devmeta:web"])   # or "/"
def homepage():
    return {"page": "devmeta home"}
