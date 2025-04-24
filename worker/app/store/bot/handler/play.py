import asyncio
from typing import TYPE_CHECKING

from app.game.accessor import NewPlayer
from app.game.models import Game, GameStatus, TrackColor
from app.store.bot.handler.base_handler import BaseHandler
from app.store.bot.handler.shared import (
    create_callback,
    game_settings_text,
    player_to_md,
    players_to_md,
)
from app.store.bot.types import InlineButtonType
from app.store.tg_api.dataclasses import (
    CallbackUpdate,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Reply,
    Sender,
    Update,
)

if TYPE_CHECKING:
    from app.web.app import Application


class PlayHandler(BaseHandler):
    time_for_prepare = 60
    warning_time = 10

    def __init__(self, app: "Application"):
        super().__init__(app)
        self.prepare_timers: dict[int, asyncio.Task] = {}
        self.keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Начать",
                        callback_data=InlineButtonType.REGISTRATION,
                    ),
                    InlineKeyboardButton(
                        text="Настройки",
                        callback_data=InlineButtonType.SETTINGS,
                    ),
                    InlineKeyboardButton(
                        text="Отменить",
                        callback_data=InlineButtonType.CANCEL,
                    ),
                ]
            ]
        )

    async def handle(self, update: Update | CallbackUpdate) -> Reply | None:
        if isinstance(update, Update):
            chat_id = update.message.chat.id
            user = update.message.sender
            message_id = update.message.message_id + 1
        else:
            chat_id = update.callback_query.message.chat.id
            user = update.callback_query.sender
            message_id = update.callback_query.message.message_id

        game = await self.app.store.game.get_latest_game(chat_id)
        if game and game.status == GameStatus.ACTIVE:
            reply = await self.warning_reply(chat_id, game.id, "Игра еще идет")
        elif game and game.status == GameStatus.PREPARATION:
            reply = await self.warning_reply(
                chat_id,
                game.id,
                "Идет подготовка к игре",
            )
        elif game and game.status == GameStatus.REGISTRATION:
            reply = await self.warning_reply(
                chat_id,
                game.id,
                "Идет регистрация на игру",
                participants=True,
                invite=True,
            )
        elif not game or game.status == GameStatus.FINISHED:
            reply = await self.prepare_game(chat_id, user, message_id)
        return reply

    async def warning_reply(
        self,
        chat_id: int,
        game_id: int,
        warning: str,
        invite: bool = False,
        participants: bool = False,
    ) -> Reply:
        text = warning

        if participants:
            players = await self.app.store.game.get_players_by_game_id(game_id)
            if players:
                text += "\n\nПрисоединились:"
                text += players_to_md(players)

        keyboard = None

        if invite:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Участвовать",
                            callback_data=InlineButtonType.REGISTRATION,
                        )
                    ]
                ]
            )

        return Reply(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode="Markdown",
        )

    def create_reply(self, chat_id: int, message_id: int, game: Game) -> Reply:
        text = "Скоро начнем регистрацию на игру! \n\n"
        text += f"Настройкой занимается {player_to_md(game.manager)}\n"
        text += game_settings_text(game)

        return Reply(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=self.keyboard,
            parse_mode="Markdown",
        )

    async def prepare_game(
        self, chat_id: int, manager: Sender, message_id: int | None
    ) -> Reply:
        new_player: NewPlayer = {
            "tg_id": manager.id,
            "first_name": manager.first_name,
            "last_name": manager.last_name,
            "track": TrackColor.random(),
        }

        game = await self.app.store.game.create_game(chat_id, new_player)

        await self._start_prepare_timer(chat_id, game.id, manager, message_id)

        return self.create_reply(chat_id, message_id, game)

    async def _start_prepare_timer(
        self, chat_id: int, game_id: int, manager: Sender, message_id: int
    ):
        if chat_id in self.prepare_timers:
            self.prepare_timers[chat_id].cancel()
            del self.prepare_timers[chat_id]

        warning_task = asyncio.create_task(
            self._send_prepare_warning(chat_id, game_id)
        )
        end_task = asyncio.create_task(
            self._cancel_game(chat_id, game_id, manager, message_id)
        )

        self.prepare_timers[chat_id] = asyncio.gather(warning_task, end_task)

    async def _send_prepare_warning(self, chat_id: int, game_id: int):
        try:
            await asyncio.sleep(self.time_for_prepare - self.warning_time)

            game = await self.app.store.game.get_game_by_id(game_id)
            if game and game.status == GameStatus.PREPARATION:
                await self.app.store.tg_api.send_message(
                    Reply(
                        chat_id=chat_id,
                        text=(
                            "Запустите игру, иначе она будет "
                            f"отменена через {self.warning_time} секунд!"
                        ),
                    )
                )
        except asyncio.CancelledError:
            pass
        finally:
            if chat_id in self.prepare_timers:
                del self.prepare_timers[chat_id]

    async def _cancel_game(
        self, chat_id: int, game_id: int, manager: Sender, message_id: int
    ):
        try:
            await asyncio.sleep(self.time_for_prepare)

            if chat_id in self.prepare_timers:
                del self.prepare_timers[chat_id]

            game = await self.app.store.game.get_game_by_id(game_id)
            if game and game.status == GameStatus.PREPARATION:
                await self.app.store.game.update_status_latest_game(
                    chat_id, GameStatus.CANCELED
                )
                callback_update = create_callback(
                    chat_id, message_id, manager, InlineButtonType.HOME
                )

                accessor = self.app.store.bot_manager
                reply = await accessor.start_handler.handle(callback_update)
                await self.app.store.tg_api.edit_message(reply)
        except asyncio.CancelledError:
            pass
        finally:
            if chat_id in self.prepare_timers:
                del self.prepare_timers[chat_id]
