import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.quiz.models import Question
from app.store.database.sqlalchemy_base import BaseModel


class GameStatus(enum.Enum):
    active = "active"
    finished = "finished"


class TrackColor(enum.Enum):
    red = "red"
    yellow = "yellow"
    green = "green"


class Game(BaseModel):
    __tablename__ = "Game"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    winner_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(
            "GamePlayer.id",
            use_alter=True,
            name="fk_game_winner_id",
            deferrable=True,
        ),
        nullable=True,
    )
    status: Mapped[GameStatus] = mapped_column(
        Enum(GameStatus), nullable=False, server_default=GameStatus.active.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    winner: Mapped["GamePlayer | None"] = relationship(
        "GamePlayer", foreign_keys=[winner_id]
    )
    game_rounds: Mapped[list["GameRound"]] = relationship(
        "GameRound", back_populates="game"
    )
    players: Mapped[list["GamePlayer"]] = relationship(
        "GamePlayer", foreign_keys="[GamePlayer.game_id]"
    )


class GamePlayer(BaseModel):
    __tablename__ = "GamePlayer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Game.id"), nullable=False
    )
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    track: Mapped[TrackColor] = mapped_column(Enum(TrackColor), nullable=False)
    correct_answers: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    incorrect_answers: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    in_game: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="true"
    )


class GameRound(BaseModel):
    __tablename__ = "GameRound"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Game.id"), nullable=False
    )
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Question.id"), nullable=False
    )
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("GamePlayer.id"), nullable=False
    )
    answer: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    game: Mapped["Game"] = relationship("Game", back_populates="game_rounds")
    question: Mapped["Question"] = relationship("Question")
    player: Mapped["GamePlayer"] = relationship("GamePlayer")
