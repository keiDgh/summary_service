from sqlalchemy import Integer, UUID as SA_UUID, String, Text
from sqlalchemy.orm import mapped_column, Mapped

from app.infra.db.base import Base

from uuid import UUID, uuid4

class Summary(Base):
    __tablename__ = "summaries"

    summary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    public_summary_id: Mapped[UUID] = mapped_column(SA_UUID, default=uuid4, unique=True)
    resource_key: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    author: Mapped[str | None] = mapped_column(String, nullable=True, server_default=None)