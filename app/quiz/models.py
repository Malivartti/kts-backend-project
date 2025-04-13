import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.store.database.sqlalchemy_base import BaseModel


class QuestionType(enum.Enum):
    single = "single"
    multi = "multi"


class Theme:
    __tablename__ = "Theme"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)


class Question(BaseModel):
    __tablename__ = "Question"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    theme_id = Column(Integer, ForeignKey("Theme.id"), nullable=False)
    title = Column(String, nullable=False)
    type = Column(Enum(QuestionType), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question")


class Answer(BaseModel):
    __tablename__ = "Answer"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("Question.id"), nullable=False)
    title = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    question = relationship("Question", back_populates="answers")
