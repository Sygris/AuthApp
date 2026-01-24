from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    nickname: str | None = None
