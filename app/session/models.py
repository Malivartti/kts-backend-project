from sqlalchemy import Column, DateTime, String

from app.store.database.sqlalchemy_base import BaseModel


class Session(BaseModel):
    __tablename__ = "Session"

    session_key = Column(String, primary_key=True)
    session_data = Column(String, nullable=False)
    expire_date = Column(DateTime, nullable=False)
