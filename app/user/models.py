from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)

from app.store.database.sqlalchemy_base import BaseModel


class User(BaseModel):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, server_default="false")
    last_login = Column(DateTime, nullable=True)
