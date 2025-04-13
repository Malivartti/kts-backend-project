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


class GameStatus(enum.Enum):
    active = "active"
    finished = "finished"


class TrackColor(enum.Enum):
    red = "red"
    yellow = "yellow"
    green = "green"


class Game(BaseModel):
    __tablename__ = "Game"

    id = Column(Integer, primary_key=True)
    tg_group_id = Column(Integer, nullable=False)
    winner_id = Column(Integer, ForeignKey("GamePlayer.id"), nullable=True)
    status = Column(
        Enum(GameStatus), nullable=False, server_default=GameStatus.active.value
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    winner = relationship("GamePlayer")
    game_rounds = relationship("GameRound", back_populates="game")
    players = relationship("GamePlayer", back_populates="game")


class GamePlayer(BaseModel):
    __tablename__ = "GamePlayer"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("Game.id"), nullable=False)
    tg_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    track = Column(Enum(TrackColor), nullable=False)
    correct_answers = Column(Integer, nullable=False, server_default="0")
    incorrect_answers = Column(Integer, nullable=False, server_default="0")
    in_game = Column(Boolean, nullable=False, server_default="true")

    game = relationship("Game", back_populates="players")


class GameRound(BaseModel):
    __tablename__ = "GameRound"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("Game.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("Question.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("GamePlayer.id"), nullable=False)
    answer = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    game = relationship("Game", back_populates="game_rounds")
    question = relationship("Question", back_populates="game_rounds")
    player = relationship("GamePlayer", back_populates="game_rounds")
