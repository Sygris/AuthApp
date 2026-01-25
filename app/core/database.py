import os
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

# Gets value of DATABASE_URL set in the .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not set stop the application
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL: Not set")

# Creates the engine which manages connections to the database
engine = create_engine(DATABASE_URL, echo=True)  # echo used for debug

# Creates a session object which is used to interact with the database
SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)


# Parent class for every ORM class
class Base(DeclarativeBase):
    pass


# Returns a Session which allows to interact with the database
def get_db() -> Generator[Session]:
    # creates the Session object
    db = SessionLocal()
    try:
        # Yield the database session to the request handler
        # Execution pauses here and resumes after the request finishes
        yield db
    finally:
        # Always close the session even if an exception occourred
        db.close()
