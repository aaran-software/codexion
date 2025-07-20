from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
async def auth_home():
    return {"message": "Welcome to Auth"}