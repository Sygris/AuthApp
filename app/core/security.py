import os
import secrets
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.models.user import Role as UserRole, UserDB
from app.core.database import get_db

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Password Hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

if not SECRET_KEY or not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise RuntimeError("Secret key or access token expire minutes not set")


def create_access_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = data.copy()
    payload["exp"] = expire

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_token_data(token: str = Depends(oauth2_scheme)) -> dict:
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_refresh_token():
    return secrets.token_urlsafe(64)  # 64 bytes


def get_current_user(
    token_data: dict = Depends(get_token_data), db: Session = Depends(get_db)
) -> UserDB:
    user_id = token_data.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="User not found")

    user = db.get(UserDB, user_id)

    if not user:
        raise HTTPException(status_code=401)

    return user


def require_role(required_role: UserRole):
    def dependency(current_user: UserDB = Depends(get_current_user)) -> UserDB:
        print(current_user)
        if current_user.role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient Permissions")

        return current_user

    return dependency
