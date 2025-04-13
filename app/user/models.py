from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.store.database.sqlalchemy_base import BaseModel


class User(BaseModel):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, server_default="false")
    last_login = Column(DateTime, nullable=False, server_default=func.now())

    questions = relationship("Question", back_populates="user")


class Session(BaseModel):
    __tablename__ = "Session"

    session_key = Column(String, primary_key=True)
    session_data = Column(String, nullable=False)
    expire_date = Column(DateTime, nullable=False)
