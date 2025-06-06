import random
from datetime import datetime

from app.base.types import BaseEnum
from app.quiz.models import Question, Theme
from app.store.database.sqlalchemy_base import BaseModel
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class GameStatus(BaseEnum):
    PREPARATION = "PREPARATION"
    REGISTRATION = "REGISTRATION"
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


class TrackColor(BaseEnum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

    @classmethod
    def random(cls) -> "TrackColor":
        return random.choice(list(cls))


class Game(BaseModel):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_group_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, index=True
    )
    status: Mapped[GameStatus] = mapped_column(
        Enum(GameStatus, name="game_status"),
        nullable=False,
        server_default=GameStatus.PREPARATION.value,
    )
    manager_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "game_player.id",
            use_alter=True,
            name="fk_game_manager_id",
            deferrable=True,
        ),
        nullable=True,
    )
    time_for_answer: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="20"
    )
    time_for_game: Mapped[int] = mapped_column(Integer, nullable=True)
    theme_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("theme.id"), nullable=True
    )
    winners: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    reg_start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
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
    manager: Mapped["GamePlayer | None"] = relationship(
        "GamePlayer", foreign_keys=[manager_id], lazy="noload"
    )
    theme: Mapped["Theme"] = relationship("Theme")
    game_rounds: Mapped[list["GameRound"]] = relationship(
        "GameRound", back_populates="game"
    )
    players: Mapped[list["GamePlayer"]] = relationship(
        "GamePlayer", foreign_keys="[GamePlayer.game_id]"
    )


class GamePlayer(BaseModel):
    __tablename__ = "game_player"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    game_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("game.id"),
        nullable=False,
        index=True,
    )
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    track: Mapped[TrackColor] = mapped_column(
        Enum(TrackColor, name="track_color"), nullable=False
    )
    correct_answers: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    incorrect_answers: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    in_game: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="true"
    )
    place: Mapped[int | None] = mapped_column(Integer, nullable=True)


class GameRound(BaseModel):
    __tablename__ = "game_round"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    game_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("game.id"),
        nullable=False,
        index=True,
    )
    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("question.id"),
        nullable=False,
        index=True,
    )
    player_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("game_player.id"),
        nullable=False,
        index=True,
    )
    answer: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    game: Mapped["Game"] = relationship("Game", back_populates="game_rounds")
    question: Mapped["Question"] = relationship("Question")
    player: Mapped["GamePlayer"] = relationship("GamePlayer")
