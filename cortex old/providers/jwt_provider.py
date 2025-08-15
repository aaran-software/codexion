# providers/jwt_provider.py

from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from cortex.services import ServiceProvider
from cortex.container import container
from cortex.core.settings import get_settings
from cortex.models.token import Token


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class JWTManager:
    def __init__(self, secret: str, algorithm: str, expires_minutes: int):
        self.secret = secret
        self.algorithm = algorithm
        self.expires_delta = timedelta(minutes=expires_minutes)

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or self.expires_delta)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            return username
        except JWTError:
            raise credentials_exception

    def is_token_blacklisted(self, token: str, db: Session) -> bool:
        return db.query(Token).filter_by(token=token).first() is not None

    def blacklist_token(self, token: str, user_id: int, db: Session):
        if not self.is_token_blacklisted(token, db):
            db_token = Token(token=token, user_id=user_id)
            db.add(db_token)
            db.commit()


class JWTServiceProvider(ServiceProvider):
    def register(self):
        settings = get_settings()
        jwt_manager = JWTManager(
            secret=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
            expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        container.instance("jwt", jwt_manager)

    def boot(self):
        print("🔐 JWT system booted.")
