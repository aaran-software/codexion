# cortex/routes/api.py

from fastapi import APIRouter

from apps.cxsun.core.routes import api
from cortex.DTO.dal import get_db, settings
from cortex.controllers import auth_controller
from fastapi import APIRouter, Depends
from cortex.core.security import get_current_user, oauth2_scheme
from cortex.github.git_update import GitSync
from cortex.models.token import Token
from cortex.models.user import User

router = APIRouter()

router.include_router(auth_controller.router, prefix="", tags=["auth"])
router.include_router(api.router, prefix="", tags=["purchases"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is reachable"}


@router.get("/update")
async def get_update():
    try:
        result = GitSync().sync()
        return result
    except Exception as e:
        return {"error": str(e)}


from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Request

# @router.get("/protected")
# def protected_route(current_user: User = Depends(get_current_user)):
#     return {"message": f"Hello, {current_user.username},{current_user.email}"}

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
    }

