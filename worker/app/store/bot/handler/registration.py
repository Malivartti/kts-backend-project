import asyncio
from typing import TYPE_CHECKING

from app.game.accessor import NewPlayer
from app.game.models import Game, GameStatus, TrackColor
from app.store.bot.handler.base_handler import (
    BaseInlineButtonHandler,
)
from app.store.bot.handler.shared import (
    game_reg_settings_text,
    players_to_md,
)
from app.store.bot.types import InlineButtonType
from app.store.tg_api.dataclasses import (
    CallbackUpdate,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Reply,
)

if TYPE_CHECKING:
    from app.web.app import Application


class RegistraionHandler(BaseInlineButtonHandler):
    time_for_reg = 15
    warning_time = 5
    registration_timers = {}

    def __init__(self, app: "Application"):
        super().__init__(app)
        self.keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Участвовать",
                        callback_data=InlineButtonType.REGISTRATION,
                    )
                ]
            ]
        )

    async def handle(self, update: CallbackUpdate) -> Reply | None:
        chat_id = update.callback_query.message.chat.id
        user_id = update.callback_query.sender.id

        game = await self.app.store.game.get_latest_game(chat_id)

        reply = None
        if (
            game.status == GameStatus.PREPARATION
            and game.manager.tg_id == user_id
        ):
            reply = await self.start_reg(chat_id, update)
        elif game.status == GameStatus.REGISTRATION:
            reply = await self.joining_participants(chat_id, game, update)
        return reply

    async def start_reg(self, chat_id: int, update: CallbackUpdate) -> Reply:
        game = await self.app.store.game.update_status_latest_game(
            chat_id, GameStatus.REGISTRATION
        )

        await self._start_registration_timer(chat_id, game)

        text = "Присоединяйся к игре!\n\n" + game_reg_settings_text(game)

        return Reply(
            chat_id=chat_id,
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=self.keyboard,
        )

    async def joining_participants(
        self, chat_id: int, game: Game, update: CallbackUpdate
    ) -> Reply | None:
        game_id = game.id
        contender = update.callback_query.sender
        players = await self.app.store.game.get_players_by_game_id(game_id)
        if any(player.tg_id == contender.id for player in players):
            return None

        new_player: NewPlayer = {
            "tg_id": contender.id,
            "first_name": contender.first_name,
            "last_name": contender.last_name,
            "track": TrackColor.random(),
        }

        await self.app.store.game.create_player(game_id, new_player)

        players = await self.app.store.game.get_players_by_game_id(game_id)

        text = "Присоединяйся к игре!\n\n" + game_reg_settings_text(game)
        if players:
            text += "\n\nПрисоединились:"
            text += players_to_md(players)

        return Reply(
            chat_id=chat_id,
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=self.keyboard,
            parse_mode="Markdown",
        )

    async def _start_registration_timer(self, chat_id: int, game: Game):
        if chat_id in self.registration_timers:
            self.registration_timers[chat_id].cancel()
            del self.registration_timers[chat_id]

        warning_task = asyncio.create_task(
            self._send_registration_warning(chat_id, game.id)
        )
        end_task = asyncio.create_task(self._end_registration(chat_id, game.id))

        self.registration_timers[chat_id] = asyncio.gather(
            warning_task, end_task
        )

    async def _send_registration_warning(self, chat_id: int, game_id: int):
        try:
            await asyncio.sleep(self.time_for_reg - self.warning_time)

            game = await self.app.store.game.get_game_by_id(game_id)
            if game and game.status == GameStatus.REGISTRATION:
                accessor = self.app.store.game
                players = await accessor.get_players_by_game_id(game_id)

                warning_text = (
                    f"Осталось {self.warning_time} "
                    "секунд до окончания регистрации!"
                )
                if players:
                    warning_text += "\n\nУчастники:"
                    warning_text += players_to_md(players)

                await self.app.store.tg_api.send_message(
                    Reply(
                        chat_id=chat_id,
                        text=warning_text,
                        reply_markup=self.keyboard,
                        parse_mode="Markdown",
                    )
                )
        except asyncio.CancelledError:
            pass
        finally:
            if chat_id in self.registration_timers:
                del self.registration_timers[chat_id]

    async def _end_registration(self, chat_id: int, game_id: int):
        try:
            await asyncio.sleep(self.time_for_reg)

            if chat_id in self.registration_timers:
                del self.registration_timers[chat_id]

            game = await self.app.store.game.get_game_by_id(game_id)
            if game and game.status == GameStatus.REGISTRATION:
                accessor = self.app.store.game
                players = await accessor.get_players_by_game_id(game.id)

                if not players:
                    await self.app.store.game.update_status_latest_game(
                        chat_id, GameStatus.CANCELED
                    )
                    await self.app.store.tg_api.send_message(
                        Reply(
                            chat_id=chat_id,
                            text="Игра отменена: никто не присоединился.",
                        )
                    )
                else:
                    await self.app.store.game.update_status_latest_game(
                        chat_id, GameStatus.ACTIVE
                    )

                    start_text = (
                        "Регистрация завершена! Игра начинается!\n\nУчастники:"
                    )
                    start_text += players_to_md(players, with_track=True)

                    await self.app.store.tg_api.send_message(
                        Reply(
                            chat_id=chat_id,
                            text=start_text,
                            parse_mode="Markdown",
                        )
                    )

                    accessor = self.app.store.bot_manager
                    await self.app.store.tg_api.send_message(
                        await accessor.game_message_handler.start_game(
                            chat_id, game
                        )
                    )
        except asyncio.CancelledError:
            pass
        finally:
            if chat_id in self.registration_timers:
                del self.registration_timers[chat_id]
