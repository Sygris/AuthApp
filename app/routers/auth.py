from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserDB
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.core.security import hash_password, verify_password

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


@authRouter.post("/login")
def login(loginData: UserLogin, db: Session = Depends(get_db)):
    # Gets user from database based on email
    stmt = select(UserDB).where(UserDB.email == loginData.email)
    existing_user = db.execute(stmt).scalar_one_or_none()

    # If there is no user in the database with the email used to login
    # abort the request and send a HTTPException
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # If the password used to login is wrong
    # abort the request and send a HTTPException
    if not verify_password(loginData.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"login": "ok"}
