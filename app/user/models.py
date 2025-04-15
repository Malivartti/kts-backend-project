from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.store.database.sqlalchemy_base import BaseModel


class User(BaseModel):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
