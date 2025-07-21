# cortex/routes/api.py

from fastapi import APIRouter

from cortex.DTO.dal import get_db
from cortex.controllers import auth_controller
from fastapi import APIRouter, Depends
from cortex.core.security import get_current_user, oauth2_scheme
from cortex.models.token import Token
from cortex.models.user import User

router = APIRouter()

router.include_router(auth_controller.router, prefix="", tags=["Auth"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is reachable"}

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Request

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}"}
