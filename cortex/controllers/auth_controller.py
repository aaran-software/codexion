# cortex/controllers/auth_controller.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from cortex.models.user import User
from cortex.DTO.dal import get_db
from cortex.database.schemas.auth import LoginRequest
from cortex.core.hashing import verify_password  # Make sure this is imported
from cortex.core.jwt_handler import create_access_token
from cortex.core.logger import logger

router = APIRouter()
import logging

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.username == data.username).first()
        if not user:
            logger.warning("Login failed: no such user %s", data.username)
            raise HTTPException(401, "Invalid credentials")

        if not verify_password(data.password, user.password):
            logger.warning("Login failed: wrong password for %s", data.username)
            raise HTTPException(401, "Invalid credentials")

        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in login")
        raise HTTPException(500, "Internal server error")

