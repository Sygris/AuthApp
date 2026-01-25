from app.core.database import engine, Base

# All models need to be imported in order to be created in the database
from app.models.user import UserDB


def create_tables():
    Base.metadata.create_all(bind=engine)
