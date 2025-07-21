# cortex/controllers/auth_controller.py
from fastapi import APIRouter, HTTPException, Depends, Request
from jose import jwt, JWTError, ExpiredSignatureError
from starlette import status

from cortex.models.token import Token
from cortex.models.user import User
from cortex.DTO.dal import get_db
from cortex.database.schemas.auth import LoginRequest
from cortex.core.hashing import verify_password  # Make sure this is imported
from cortex.core.jwt_handler import create_access_token
from cortex.core.logger import logger
from cortex.core.config import get_settings
from sqlalchemy.orm import Session
from cortex.database.schemas import user
from cortex.core import hashing

router = APIRouter()

settings = get_settings()
@router.post("/signup")
def signup(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    hashed_pw = hashing.hash_password(user.password)
    new_user = User(username=user.username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

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

        print(token)
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in login")
        raise HTTPException(500, "Internal server error")

@router.post("/logout")
def logout(request: Request, db: Session = Depends(get_db)):
    try:
        token = extract_token_from_request(request)  # From header/cookie
        user_id = get_user_id_from_token(token, db, verify=False)  # skip strict verify
        db_token = Token(token=token, user_id=user_id)
        db.add(db_token)
        db.commit()
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Logout failed or invalid token")


# logout purpose
def extract_token_from_request(request: Request) -> str:
    """Extracts the Bearer token from Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    return auth_header.split(" ")[1]


def get_user_id_from_token(token: str, db: Session, verify: bool = True):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_signature": verify} if not verify else None,
        )
        return payload.get("sub")  # or however you store user_id
    except ExpiredSignatureError:
        payload = jwt.get_unverified_claims(token)
        return payload.get("sub")  # fallback for expired but valid tokens
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")