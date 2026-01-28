from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from app.core.security import get_current_user
from app.schemas.user import UserPublic
from app.utils.init_db import create_tables
from app.routers.auth import authRouter
from app.models.user import UserDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initialising the database...")
    create_tables()
    print("Database has been initialised")
    yield
    print("Closing application")


app = FastAPI(lifespan=lifespan)

# Add routers to app
app.include_router(authRouter)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/profile", response_model=UserPublic)
def profile(current_user: UserDB = Depends(get_current_user)):
    return current_user
