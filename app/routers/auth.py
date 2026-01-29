from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserDB
from app.schemas.user import RefreshRequest, UserCreate, UserLogin, UserPublic, Token
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    hash_password,
    verify_password,
)

authRouter = APIRouter(prefix="/auth", tags=["auth"])


@authRouter.post("/signup", response_model=UserPublic)
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


@authRouter.post("/login", response_model=Token)
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

    # Creates access token (short lived) and refresh token (long lived/stored in db)
    access_token = create_access_token(
        {"sub": str(existing_user.id), "role": existing_user.role.value}
    )
    refresh_token = create_refresh_token()

    # Saves it in the db
    existing_user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@authRouter.post("/logout")
def logout(
    current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)
):
    current_user.refresh_token = None
    db.commit()

    return {"logout": "ok"}


@authRouter.post("/refresh")
def refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):
    stmt = select(UserDB).where(UserDB.refresh_token == data.refresh_token)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Refresh Token")

    new_access_token = create_access_token({"sub": user.id, "role": user.role})

    return {"access_token": new_access_token, "token_type": "bearer"}
