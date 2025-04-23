import asyncio
from typing import TYPE_CHECKING

from app.game.accessor import UpdateGamePlayer
from app.game.models import GameStatus
from app.quiz.models import QuestionType
from app.store.bot.handler.base_handler import BaseCommandHandler
from app.store.bot.types import track_conditions
from app.store.tg_api.dataclasses import (
    KeyboardButton,
    Reply,
    ReplyKeyboardMarkup,
    Update,
)

if TYPE_CHECKING:
    from app.web.app import Application


class GameMessageHandler(BaseCommandHandler):
    active_games: dict[int, asyncio.Task] = {}
    active_rounds: dict[int, asyncio.Task] = {}
    time_to_play = 2  # minutes
    time_to_reply = 20  # seconds
    remove_keyboard = ReplyKeyboardMarkup(remove_keyboard=True, selective=False)

    def __init__(self, app: "Application"):
        super().__init__(app)

    async def handle(self, update: Update) -> list[Reply]:
        chat_id = update.message.chat.id

        game = await self.app.store.game.get_latest_game(chat_id)
        if game.status != GameStatus.ACTIVE:
            return []

        game_round = await self.app.store.game.get_latest_game_round_by_game_id(
            game.id
        )

        if game_round.player.tg_id != update.message.sender.id:
            return []

        if game_round.id in self.active_rounds:
            self.active_rounds[game_round.id].cancel()
            del self.active_rounds[game_round.id]

        return [
            await self.handle_message(
                chat_id, update.message.text, game_round, game
            ),
            await self.send_reply(chat_id, game.id),
        ]

    async def handle_message(
        self, chat_id: int, player_answer, game_round, game
    ) -> Reply:
        await self.app.store.game.save_answer_by_round_id(
            game_round.id, player_answer
        )
        correct_answer = (
            await self.app.store.quiz.get_correct_answer_by_question_id(
                game_round.question_id
            )
        )
        game_player = game_round.player
        is_correct = (
            str(player_answer).strip().lower() == str(correct_answer).lower()
        )

        player_fields_to_update: UpdateGamePlayer = {}
        if is_correct:
            response_text = f"Правильно! Вы дали верный ответ: {player_answer}."
            if (
                game_player.correct_answers + game_player.incorrect_answers + 1
            ) == track_conditions[game_player.track]["distance"]:
                player_place = game.winners + 1
                response_text += (
                    "\nВы достигли конца своей дорожки "
                    f"и занимаете {player_place} место!"
                )
                await self.app.store.game.update_game_winners_by_game_id(
                    game.id,
                    player_place,
                )
                player_fields_to_update["in_game"] = False
                player_fields_to_update["place"] = player_place
            player_fields_to_update["correct_answers"] = (
                game_player.correct_answers + 1
            )
        else:
            response_text = f"Неправильно. Правильный ответ: {correct_answer}."
            if (
                game_player.incorrect_answers + 1
                > track_conditions[game_player.track]["mistakes"]
            ):
                response_text += (
                    "\nВы достигли максимум ошибок "
                    "для своей дорожки и выбываете из игры"
                )
                player_fields_to_update["in_game"] = False
            player_fields_to_update["incorrect_answers"] = (
                game_player.incorrect_answers + 1
            )
        await self.app.store.game.update_game_player_by_id(
            game_player.id, player_fields_to_update
        )

        return Reply(
            chat_id=chat_id,
            text=response_text,
            reply_markup=self.remove_keyboard,
        )

    async def send_reply(
        self, chat_id: int, game_id: int, theme_id: int | None = None
    ) -> Reply:
        next_player = await self.app.store.game.get_next_game_player(game_id)
        if not next_player:
            await self._finish_game(chat_id, game_id)
            return Reply(
                chat_id=chat_id,
                text="Игра завершена! Все игроки выбыли.",
                reply_markup=self.remove_keyboard,
            )

        next_question = await self.app.store.game.get_unique_random_question(
            game_id, theme_id
        )
        if not next_question:
            await self._finish_game(chat_id, game_id)
            return Reply(
                chat_id=chat_id,
                text="Игра завершена! Вопросы закончились.",
                reply_markup=self.remove_keyboard,
            )

        game_round = await self.app.store.game.create_game_round(
            game_id, next_player.id, next_question.id
        )

        text = "Вопрос для "
        player_name = next_player.first_name
        if next_player.last_name:
            player_name += " " + next_player.last_name

        player_link = f"[{player_name}](tg://user?id={next_player.tg_id})"
        text += f"{player_link}"
        text += f"\n{next_question.title}"

        self.active_rounds[game_round.id] = asyncio.create_task(
            self._reply_timer(chat_id, game_id, game_round.id)
        )

        reply = Reply(
            chat_id=chat_id,
            text=text,
            parse_mode="Markdown",
        )

        if next_question.type == QuestionType.MULTI:
            answers = await self.app.store.quiz.get_answers_by_question_id(
                next_question.id
            )
            buttons = []
            for answer in answers:
                button = KeyboardButton(text=answer.title)
                buttons.append([button])

            keyboard = ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True,
                one_time_keyboard=True,
                selective=True,
            )

            reply.reply_markup = keyboard
        return reply

    async def start_game(
        self, chat_id: int, game_id: int, theme_id: int | None = None
    ) -> Reply:
        self.active_games[game_id] = asyncio.create_task(
            self._game_timer(chat_id)
        )

        return await self.send_reply(chat_id, game_id, theme_id)

    async def _game_timer(self, chat_id: int):
        await asyncio.sleep(self.time_to_play * 60)

        game = await self.app.store.game.get_latest_game(chat_id)
        try:
            if game and game.status == GameStatus.ACTIVE:
                await self._finish_game(chat_id, game.id)
                await self.app.store.tg_api.send_message(
                    Reply(
                        chat_id=chat_id,
                        text="Время игры истекло! Игра завершена.",
                        reply_markup=self.remove_keyboard,
                    )
                )
        except asyncio.CancelledError:
            pass
        finally:
            if game.id in self.active_games:
                del self.active_games[game.id]

    async def _reply_timer(self, chat_id: int, game_id: int, round_id: int):
        try:
            await asyncio.sleep(self.time_to_reply)
            game = await self.app.store.game.get_latest_game(chat_id)
            if game and game.status == GameStatus.ACTIVE:
                game_round = (
                    await self.app.store.game.get_latest_game_round_by_game_id(
                        game.id
                    )
                )
                player = game_round.player
                player_fields_to_update: UpdateGamePlayer = {
                    "incorrect_answers": player.incorrect_answers + 1
                }
                correct_answer = (
                    await self.app.store.quiz.get_correct_answer_by_question_id(
                        game_round.question_id
                    )
                )
                timeout_message = (
                    "Время ответа истекло! "
                    f"Правильный ответ: {correct_answer}."
                )
                if (
                    player.incorrect_answers + 1
                    > track_conditions[player.track]["mistakes"]
                ):
                    player_fields_to_update["in_game"] = False
                    timeout_message += (
                        "\nВы достигли максимум ошибок "
                        "для своей дорожки и выбываете из игры"
                    )
                await self.app.store.game.update_game_player_by_id(
                    player.id, player_fields_to_update
                )

                await self.app.store.tg_api.send_message(
                    Reply(
                        chat_id=chat_id,
                        text=timeout_message,
                        reply_markup=self.remove_keyboard,
                    )
                )

                await self.app.store.tg_api.send_message(
                    await self.send_reply(chat_id, game_id)
                )

        except asyncio.CancelledError:
            pass
        finally:
            if round_id in self.active_rounds:
                del self.active_rounds[round_id]

    async def _finish_game(self, chat_id: int, game_id: int):
        await self.app.store.game.update_status_latest_game(
            chat_id, GameStatus.FINISHED
        )

        if game_id in self.active_games:
            self.active_games[game_id].cancel()
            del self.active_games[game_id]
