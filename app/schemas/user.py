from pydantic import BaseModel, EmailStr

from app.models.user import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str | None = None
    role: Role | None = None


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    nickname: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshRequest(BaseModel):
    refresh_token: str
