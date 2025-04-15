import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.store.database.sqlalchemy_base import BaseModel


class QuestionType(enum.Enum):
    single = "single"
    multi = "multi"


class Theme(BaseModel):
    __tablename__ = "Theme"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="theme"
    )


class Question(BaseModel):
    __tablename__ = "Question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("User.id"), nullable=False
    )
    theme_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Theme.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    theme: Mapped["Theme"] = relationship("Theme", back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(
        "Answer", back_populates="question"
    )


class Answer(BaseModel):
    __tablename__ = "Answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Question.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    question: Mapped["Question"] = relationship(
        "Question", back_populates="answers"
    )
