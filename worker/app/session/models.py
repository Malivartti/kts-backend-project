import uuid
from datetime import datetime

from app.store.database.sqlalchemy_base import BaseModel
from sqlalchemy import UUID, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column


class Session(BaseModel):
    __tablename__ = "session"

    session_key: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )
    session_data: Mapped[str] = mapped_column(String, nullable=False)
    expire_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    __table_args__ = (
        Index("idx_session_key_expire_date", "session_key", "expire_date"),
    )
