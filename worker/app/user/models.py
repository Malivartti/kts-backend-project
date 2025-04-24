from app.store.database.sqlalchemy_base import BaseModel
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )
