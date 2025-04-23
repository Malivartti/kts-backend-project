from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.base.types import BaseEnum
from app.store.database.sqlalchemy_base import BaseModel


class QuestionType(BaseEnum):
    SINGLE = "SINGLE"
    MULTI = "MULTI"


class Theme(BaseModel):
    __tablename__ = "theme"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="theme"
    )


class Question(BaseModel):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
        index=True,
    )
    theme_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("theme.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType, name="question_type"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    theme: Mapped["Theme"] = relationship("Theme", back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(
        "Answer", back_populates="question", passive_deletes=True
    )


class Answer(BaseModel):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("question.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    question: Mapped["Question"] = relationship(
        "Question", back_populates="answers"
    )


def theme_to_dict(theme: Theme) -> dict:
    return {"id": theme.id, "title": theme.title}


def question_to_dict(question: Question) -> dict:
    return {
        "id": question.id,
        "user_id": question.user_id,
        "theme_id": question.theme_id,
        "title": question.title,
        "type": question.type.value,
        "created_at": question.created_at.isoformat(),
        "updated_at": question.updated_at.isoformat(),
    }


def answer_to_dict(answer: Answer) -> dict:
    return {
        "id": answer.id,
        "question_id": answer.question_id,
        "title": answer.title,
        "is_correct": answer.is_correct,
        "created_at": answer.created_at.isoformat(),
        "updated_at": answer.updated_at.isoformat(),
    }
