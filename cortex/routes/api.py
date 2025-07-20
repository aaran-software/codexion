# cortex/routes/api.py

from fastapi import APIRouter

from cortex.controllers import auth_controller
from fastapi import APIRouter, Depends
from cortex.core.security import get_current_user

router = APIRouter()

router.include_router(auth_controller.router, prefix="", tags=["Auth"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is reachable"}

# @router.get("/login")
# def login_get():
#     return {"message": "Use POST to login"}

@router.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}. You are authenticated."}