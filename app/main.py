from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.utils.init_db import create_tables
from app.routers.auth import authRouter


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
