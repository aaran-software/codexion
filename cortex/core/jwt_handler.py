from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from cortex.models.token import Token
from cortex.core.config import get_settings


# Exception for invalid credentials
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

settings = get_settings()
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")


def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

def is_token_blacklisted(token: str, db: Session) -> bool:
    return db.query(Token).filter_by(token=token).first() is not None

def blacklist_token(token: str, user_id: int, db: Session):
    if not is_token_blacklisted(token, db):
        db_token = Token(token=token, user_id=user_id)
        db.add(db_token)
        db.commit()
