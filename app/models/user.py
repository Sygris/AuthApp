from enum import Enum, unique
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum, func


# Throws ValueError if there are any duplicate values
@unique
class Role(Enum):
    USER = "user"
    ADMIN = "admin"


class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    nickname: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[Role] = mapped_column(SQLEnum(Role), default=Role.USER)

    refresh_token: Mapped[str | None] = mapped_column(String)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
