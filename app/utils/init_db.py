from app.core.database import engine, Base
from app.models.user import UserDB


def create_tables():
    Base.metadata.create_all(bind=engine)
