from app.core.database import engine, Base
from app.core.models.user import User


def create_tables():
    Base.metadata.create_all(bind=engine)
