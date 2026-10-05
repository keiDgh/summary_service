from sqlalchemy import Integer, UUID as SA_UUID, String
from sqlalchemy.orm import mapped_column, Mapped

from app.infra.db.base import Base

from uuid import UUID, uuid4

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    public_user_id: Mapped[UUID] = mapped_column(SA_UUID, default=uuid4, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)