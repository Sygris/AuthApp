from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import UserDB
from app.schemas.user import UserCreate, UserRead


authRouter = APIRouter()


@authRouter.post("/signup", response_model=UserRead)
def signup(signupData: UserCreate, db: Session = Depends(get_db)):
    # Checks if email is already registered in the database
    stmt = select(UserDB).where(UserDB.email == signupData.email)
    existing_user = db.execute(stmt).scalar_one_or_none()

    # If the email is already registered throw a HTTPException
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = UserDB(**signupData.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
