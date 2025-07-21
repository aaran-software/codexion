# core/security.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from cortex.DTO.dal import get_db
from cortex.core.config import get_settings
from typing import Annotated

# OAuth2 scheme pointing to the token endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

#
# def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
#     """
#     Extract and verify the JWT token, and return the username (subject).
#     Raises 401 error if the token is invalid or missing.
#     """
#     settings = get_settings()
#
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid or missing credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         payload = jwt.decode(
#             token,
#             settings.JWT_SECRET_KEY,
#             algorithms=[settings.JWT_ALGORITHM],
#         )
#         username: str | None = payload.get("sub")
#         if not username:
#             raise credentials_exception
#         return username
#     except JWTError:
#         raise credentials_exception

from cortex.models.token import Token  # ✅ your model
from sqlalchemy.orm import Session

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> str:
    settings = get_settings()

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # ✅ Check if token is blacklisted
        blacklisted = db.query(Token).filter(Token.token == token).first()
        if blacklisted:
            raise HTTPException(status_code=401, detail="Token is blacklisted")

        # ✅ Decode token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        username: str | None = payload.get("sub")
        if not username:
            raise credentials_exception

        return username

    except JWTError:
        raise credentials_exception
