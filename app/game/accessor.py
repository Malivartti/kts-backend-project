import random
from typing import TYPE_CHECKING, NotRequired, TypedDict

from sqlalchemy import desc, select, update
from sqlalchemy.orm import selectinload

from app.base.base_accessor import BaseAccessor
from app.game.models import Game, GamePlayer, GameRound, GameStatus, TrackColor
from app.quiz.models import Question

if TYPE_CHECKING:
    from app.web.app import Application


class UpdateGamePlayer(TypedDict, total=False):
    correct_answers: NotRequired[int]
    incorrect_answers: NotRequired[int]
    in_game: NotRequired[bool]
    place: NotRequired[int]


class GameAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        self.app = app

    async def create_game(self, tg_group_id: int) -> Game:
        game = Game(tg_group_id=tg_group_id)
        async with self.app.database.session() as session:
            session.add(game)
            await session.commit()
            await session.refresh(game)
        return game

    async def get_latest_game(self, tg_group_id: int) -> Game | None:
        async with self.app.database.session() as session:
            query = (
                select(Game)
                .where(Game.tg_group_id == tg_group_id)
                .order_by(desc(Game.created_at))
                .limit(1)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_games(self, tg_group_id: int | None = None) -> list[Game]:
        async with self.app.database.session() as session:
            query = select(Game)
            if tg_group_id is not None:
                query = query.where(Game.tg_group_id == tg_group_id)
            result = await session.execute(query)
            return list(result.scalars().all())

    async def create_player(
        self,
        game_id: int,
        tg_id: int,
        first_name: str,
        last_name: str | None,
        track: TrackColor,
    ) -> GamePlayer:
        player = GamePlayer(
            game_id=game_id,
            tg_id=tg_id,
            first_name=first_name,
            last_name=last_name,
            track=track,
        )
        async with self.app.database.session() as session:
            session.add(player)
            await session.commit()
            await session.refresh(player)
        return player

    async def update_status_latest_game(
        self, tg_group_id: int, status: GameStatus
    ) -> Game:
        async with self.app.database.session() as session:
            subquery = (
                select(Game)
                .where(Game.tg_group_id == tg_group_id)
                .order_by(desc(Game.created_at))
                .limit(1)
                .subquery()
            )
            query = (
                update(Game)
                .where(Game.id == subquery.c.id)
                .values(status=status)
                .execution_options(synchronize_session="fetch")
                .returning(Game)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    async def get_players_by_game_id(self, game_id: int) -> list[GamePlayer]:
        async with self.app.database.session() as session:
            query = select(GamePlayer).where(GamePlayer.game_id == game_id)
            result = await session.execute(query)
            return list(result.scalars().all())

    async def get_latest_game_round_by_game_id(
        self, game_id: int
    ) -> GameRound | None:
        async with self.app.database.session() as session:
            query = (
                select(GameRound)
                .where(GameRound.game_id == game_id)
                .options(selectinload(GameRound.player))
                .order_by(desc(GameRound.created_at))
                .limit(1)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def save_answer_by_round_id(self, round_id: int, answer: str):
        async with self.app.database.session() as session:
            query = (
                update(GameRound)
                .where(GameRound.id == round_id)
                .values(answer=answer)
            )
            await session.execute(query)
            await session.commit()

    async def update_game_player_by_id(
        self, player_id: int, fields: UpdateGamePlayer
    ):
        async with self.app.database.session() as session:
            await session.execute(
                update(GamePlayer)
                .where(GamePlayer.id == player_id)
                .values(**fields)
            )
            await session.commit()

    async def update_game_winners_by_game_id(self, game_id: int, winners: int):
        async with self.app.database.session() as session:
            await session.execute(
                update(Game).where(Game.id == game_id).values(winners=winners)
            )
            await session.commit()

    async def get_next_game_player(self, game_id: int) -> GamePlayer | None:
        game_players = await self.get_players_by_game_id(game_id)

        game_round = await self.get_latest_game_round_by_game_id(game_id)
        if not game_round:
            return game_players[0]

        prev_player_index = None
        for i, player in enumerate(game_players):
            if player.id == game_round.player_id:
                prev_player_index = i
                break

        n = len(game_players)
        for offset in range(1, n):
            next_index = (prev_player_index + offset) % n
            if game_players[next_index].in_game:
                return game_players[next_index]

        if game_players[prev_player_index].in_game:
            return game_players[prev_player_index]

        return None

    async def get_used_question_ids(self, game_id: int) -> set[int]:
        async with self.app.database.session() as session:
            query = select(GameRound.question_id).where(
                GameRound.game_id == game_id
            )
            result = await session.execute(query)
            return set(result.scalars().all())

    async def get_unique_random_question(
        self, game_id: int, theme_id: int | None = None
    ) -> Question:
        async with self.app.database.session() as session:
            query = select(Question)

            used_question_ids = await self.get_used_question_ids(game_id)
            conditions = []
            if used_question_ids:
                conditions.append(Question.id.not_in(used_question_ids))
            if theme_id:
                conditions.append(Question.theme_id == theme_id)

            if conditions:
                query = query.where(*conditions)

            result = await session.execute(query)
            questions = result.scalars().all()
            if not questions:
                return None
            return random.choice(questions)

    async def create_game_round(
        self, game_id: int, player_id: int, question_id: int
    ) -> GameRound:
        game_round = GameRound(
            game_id=game_id,
            question_id=question_id,
            player_id=player_id,
        )
        async with self.app.database.session() as session:
            session.add(game_round)
            await session.commit()
            await session.refresh(game_round)
        return game_round

    async def get_rating(self, tg_group_id: int | None = None) -> dict:
        games = await self.get_games(tg_group_id)
        player_points = {}
        for game in games:
            if game.status != GameStatus.FINISHED:
                continue

            game_players = await self.app.store.game.get_players_by_game_id(
                game.id
            )
            for player in game_players:
                if player.place is None:
                    continue
                points = 0
                if player.place == 1:
                    points = 5
                elif player.place == 2:
                    points = 3
                elif player.place == 3:
                    points = 1

                if player.tg_id in player_points:
                    player_points[player.tg_id]["points"] += points

                player_points[player.tg_id] = {
                    "tg_id": player.tg_id,
                    "first_name": player.first_name,
                    "last_name": player.last_name,
                    "points": points,
                }

        rating_list = list(player_points.values())
        rating_list.sort(key=lambda x: x["points"], reverse=True)

        return rating_list[:15]
