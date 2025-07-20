from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
async def auth_home():
    return {"message": "Welcome to Auth"}

@router.get("/status")
async def api_status():
    return {"message": "API is live"}