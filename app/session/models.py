from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.store.database.sqlalchemy_base import BaseModel


class Session(BaseModel):
    __tablename__ = "Session"

    session_key: Mapped[str] = mapped_column(String, primary_key=True)
    session_data: Mapped[str] = mapped_column(String, nullable=False)
    expire_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
