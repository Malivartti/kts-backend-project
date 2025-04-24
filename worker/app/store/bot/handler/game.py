import asyncio
from typing import TYPE_CHECKING

from app.game.accessor import UpdateGamePlayer
from app.game.models import Game, GameStatus
from app.quiz.models import QuestionType
from app.store.bot.handler.base_handler import BaseCommandHandler
from app.store.bot.handler.info import InfoCommandHandler
from app.store.bot.handler.shared import player_to_md
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
    active_game_timers: dict[int, asyncio.Task] = {}
    active_round_timers: dict[int, asyncio.Task] = {}
    remove_keyboard = ReplyKeyboardMarkup(remove_keyboard=True, selective=False)
    warning_time = 10

    def __init__(self, app: "Application"):
        super().__init__(app)

    async def handle(self, update: Update) -> list[Reply]:
        chat_id = update.message.chat.id

        game = await self.app.store.game.get_latest_game(chat_id)

        if game is None or game.status != GameStatus.ACTIVE:
            return []

        game_round = await self.app.store.game.get_latest_game_round_by_game_id(
            game.id
        )

        if game_round.player.tg_id != update.message.sender.id:
            return []

        if game_round.id in self.active_round_timers:
            self.active_round_timers[game_round.id].cancel()
            del self.active_round_timers[game_round.id]

        return [
            await self.handle_message(
                chat_id, update.message.text, game_round, game
            ),
            await self.send_reply(chat_id, game),
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
            response_text = f"Ваш ответ '{player_answer}' правильный!"
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
            response_text = f"Неверно. Правильный ответ: {correct_answer}."
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

    async def send_reply(self, chat_id: int, game: Game) -> Reply:
        game_id = game.id
        next_player = await self.app.store.game.get_next_game_player(game_id)
        if not next_player:
            await self._finish_game(chat_id, game_id)

            text = await InfoCommandHandler(self.app).create_text(
                game, "Игра завершена!"
            )
            return Reply(
                chat_id=chat_id,
                text=text,
                reply_markup=self.remove_keyboard,
                parse_mode="Markdown",
            )

        next_question = await self.app.store.game.get_unique_random_question(
            game_id, game.theme_id
        )
        if not next_question:
            await self._finish_game(chat_id, game_id)

            text = await InfoCommandHandler(self.app).create_text(
                game, "Игра завершена! Вопросы закончились."
            )

            return Reply(
                chat_id=chat_id,
                text=text,
                reply_markup=self.remove_keyboard,
                parse_mode="Markdown",
            )

        game_round = await self.app.store.game.create_game_round(
            game_id, next_player.id, next_question.id
        )

        text = "Вопрос для "

        player_md = player_to_md(next_player)
        text += f"{player_md}"
        text += f"\n{next_question.title}"

        self.active_round_timers[game_round.id] = asyncio.create_task(
            self._reply_timer(
                chat_id, game_round.id, game.id, game.time_for_answer
            )
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

    async def start_game(self, chat_id: int, game: Game) -> Reply:
        if game.time_for_game:
            await self._start_end_game_timer(
                chat_id, game.id, game.time_for_game
            )

        return await self.send_reply(chat_id, game)

    async def _start_end_game_timer(
        self, chat_id: int, game_id: int, time_for_game: int
    ):
        if game_id in self.active_game_timers:
            self.active_game_timers[game_id].cancel()
            del self.active_game_timers[game_id]

        warning_task = asyncio.create_task(
            self._send_warning_about_end_game(chat_id, game_id, time_for_game)
        )
        end_task = asyncio.create_task(
            self._game_timer(chat_id, game_id, time_for_game)
        )

        self.active_game_timers[chat_id] = asyncio.gather(
            warning_task, end_task
        )

    async def _send_warning_about_end_game(
        self, chat_id: int, game_id: int, time_for_game: int
    ):
        try:
            await asyncio.sleep(time_for_game * 60 - self.warning_time)
            game = await self.app.store.game.get_game_by_id(game_id)
            if game and game.status == GameStatus.ACTIVE:
                text = f"Игра закончится через {self.warning_time} секунд!"
                await self.app.store.tg_api.send_message(
                    Reply(
                        chat_id=chat_id,
                        text=text,
                    )
                )
        except asyncio.CancelledError:
            if game.id in self.active_game_timers:
                del self.active_game_timers[game.id]

    async def _game_timer(self, chat_id: int, game_id: int, time_for_game: int):
        try:
            await asyncio.sleep(time_for_game * 60)

            game = await self.app.store.game.get_game_by_id(game_id)
            if game and game.status == GameStatus.ACTIVE:
                await self._finish_game(chat_id, game.id)
                text = await InfoCommandHandler(self.app).create_text(
                    game, "Время игры истекло!"
                )

                await self.app.store.tg_api.send_message(
                    Reply(
                        chat_id=chat_id,
                        text=text,
                        reply_markup=self.remove_keyboard,
                        parse_mode="Markdown",
                    )
                )
        except asyncio.CancelledError:
            pass
        finally:
            if game.id in self.active_game_timers:
                del self.active_game_timers[game.id]

    async def _reply_timer(
        self, chat_id: int, round_id: int, game_id: int, time_for_answer: int
    ):
        try:
            await asyncio.sleep(time_for_answer)

            game = await self.app.store.game.get_game_by_id(game_id)
            if game and game.status == GameStatus.ACTIVE:
                game_round = (
                    await self.app.store.game.get_latest_game_round_by_game_id(
                        game.id
                    )
                )
                if round_id == game_round.id:
                    player = game_round.player
                    player_fields_to_update: UpdateGamePlayer = {
                        "incorrect_answers": player.incorrect_answers + 1
                    }
                    accessor = self.app.store.quiz
                    answer = await accessor.get_correct_answer_by_question_id(
                        game_round.question_id
                    )
                    timeout_message = (
                        "Время ответа истекло! " f"Правильный ответ: {answer}."
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
                        await self.send_reply(chat_id, game)
                    )

        except asyncio.CancelledError:
            pass
        finally:
            if round_id in self.active_round_timers:
                del self.active_round_timers[round_id]

    async def _finish_game(self, chat_id: int, game_id: int):
        await self.app.store.game.update_status_latest_game(
            chat_id, GameStatus.FINISHED
        )

        if game_id in self.active_game_timers:
            self.active_game_timers[game_id].cancel()
            del self.active_game_timers[game_id]
