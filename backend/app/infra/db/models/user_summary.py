from sqlalchemy import Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import mapped_column, Mapped

from app.infra.db.base import Base

from datetime import datetime

class UserSummaryAssociation(Base):
    __tablename__ = "user_summary_associations"

    summary_id: Mapped[int] = mapped_column(Integer, ForeignKey("summaries.summary_id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now()) 
