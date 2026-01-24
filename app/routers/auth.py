from fastapi import APIRouter

from app.schemas.user import UserCreate


authRouter = APIRouter()


@authRouter.post("/signup")
def signup(user: UserCreate):
    print(user.model_dump())
