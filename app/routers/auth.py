from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserDB
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password

authRouter = APIRouter()


@authRouter.post("/signup", response_model=UserRead)
def signup(signupData: UserCreate, db: Session = Depends(get_db)):
    # Checks if email is already registered in the database
    stmt = select(UserDB).where(UserDB.email == signupData.email)
    existing_user = db.execute(stmt).scalar_one_or_none()

    # If the email is already registered throw a HTTPException
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    signupData.password = hash_password(signupData.password)

    # Create user ORM object
    user = UserDB(**signupData.model_dump())

    # Add user object to the Session
    db.add(user)

    # Commits all changes made during the current session to the database
    db.commit()

    # Reloads the user object reflecting its most updated state in the database
    db.refresh(user)

    return user
