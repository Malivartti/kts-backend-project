import asyncio
import typing

from app.game.models import GamePlayer, GameStatus, TrackColor
from app.store.bot.handler.base_handler import BaseHandler
from app.store.bot.handler.game import GameMessageHandler
from app.store.bot.types import InlineButtonType, track_emoji
from app.store.tg_api.dataclasses import (
    CallbackUpdate,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Reply,
    Update,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


class PlayParticipateHandler(BaseHandler):
    def __init__(self, app: "Application"):
        super().__init__(app)
        self.keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Участвовать",
                        callback_data=InlineButtonType.PLAY_PARTICIPATE,
                    )
                ]
            ]
        )
        self.registration_timers = {}
        self.wait_time = 10
        self.warning_time = 5
        self.text = (
            "Присоеденяйся к игре!\n"
            f"До начала игры {self.wait_time} секунд\n"
            "Время на ответ 20 секунд"
        )

    async def handle(self, update: Update | CallbackUpdate) -> Reply | None:
        if isinstance(update, Update):
            chat_id = update.message.chat.id
        else:
            chat_id = update.callback_query.message.chat.id

        game = await self.app.store.game.get_latest_game(chat_id)
        if game and game.status == GameStatus.ACTIVE:
            reply = await self.warning_reply(chat_id, game.id, "Игра еще идет")
        elif (
            game
            and game.status == GameStatus.PREPARATION
            and isinstance(update, Update)
        ):
            reply = await self.warning_reply(
                chat_id, game.id, "Идет подготовка к игре", invite=True
            )
        elif not game or game.status == GameStatus.FINISHED:
            reply = await self.create_game(chat_id, update)
        elif game and game.status == GameStatus.PREPARATION:
            reply = await self.joining_participants(chat_id, game.id, update)
        return reply

    async def create_game(
        self, chat_id: int, update: Update | CallbackUpdate
    ) -> Reply:
        game = await self.app.store.game.create_game(chat_id)

        self._start_registration_timer(chat_id, game.id)

        return Reply(
            chat_id=chat_id,
            message_id=None
            if isinstance(update, Update)
            else update.callback_query.message.message_id,
            text=self.text,
            reply_markup=self.keyboard,
        )

    async def joining_participants(
        self, chat_id: int, game_id: int, update: CallbackUpdate
    ) -> Reply | None:
        contender = update.callback_query.sender
        players = await self.app.store.game.get_players_by_game_id(game_id)
        if any(player.tg_id == contender.id for player in players):
            return None

        await self.app.store.game.create_player(
            game_id,
            contender.id,
            contender.first_name,
            contender.last_name,
            TrackColor.random(),
        )

        players = await self.app.store.game.get_players_by_game_id(game_id)

        tmp_text = self.text
        if players:
            tmp_text += "\n\nПрисоединились:"
            tmp_text += self.players_to_markdown(players)

        return Reply(
            chat_id=chat_id,
            message_id=update.callback_query.message.message_id,
            text=tmp_text,
            reply_markup=self.keyboard,
            parse_mode="Markdown",
        )

    def players_to_markdown(
        self, players: list[GamePlayer], with_track: bool = False
    ) -> str:
        result = ""
        for player in players:
            player_name = player.first_name
            if player.last_name:
                player_name += " " + player.last_name

            player_link = f"[{player_name}](tg://user?id={player.tg_id})"
            if with_track:
                player_link += f" {track_emoji[player.track]}"
            result += f"\n{player_link}"
        return result

    async def warning_reply(
        self,
        chat_id: int,
        game_id: int,
        warning: str,
        invite: bool = False,
    ) -> Reply:
        players = await self.app.store.game.get_players_by_game_id(game_id)

        tmp_text = warning
        if players:
            tmp_text += "\n\nПрисоединились:"
            tmp_text += self.players_to_markdown(players)

        return Reply(
            chat_id=chat_id,
            text=tmp_text,
            reply_markup=self.keyboard if invite else None,
            parse_mode="Markdown",
        )

    def _start_registration_timer(self, chat_id: int, game_id: int):
        if chat_id in self.registration_timers:
            self.registration_timers[chat_id].cancel()

        warning_task = asyncio.create_task(
            self._send_registration_warning(chat_id, game_id)
        )
        end_task = asyncio.create_task(self._end_registration(chat_id, game_id))

        self.registration_timers[chat_id] = asyncio.gather(
            warning_task, end_task
        )

    async def _send_registration_warning(self, chat_id: int, game_id: int):
        await asyncio.sleep(self.warning_time)

        game = await self.app.store.game.get_latest_game(chat_id)
        if game and game.status == GameStatus.PREPARATION:
            players = await self.app.store.game.get_players_by_game_id(game_id)

            warning_text = (
                f"Осталось {self.warning_time} секунд до окончания регистрации!"
            )
            if players:
                warning_text += "\n\nУчастники:"
                warning_text += self.players_to_markdown(players)

            await self.app.store.tg_api.send_message(
                Reply(
                    chat_id=chat_id,
                    text=warning_text,
                    reply_markup=self.keyboard,
                    parse_mode="Markdown",
                )
            )

    async def _end_registration(self, chat_id: int, game_id: int):
        await asyncio.sleep(self.wait_time)

        if chat_id in self.registration_timers:
            del self.registration_timers[chat_id]

        game = await self.app.store.game.get_latest_game(chat_id)
        if game and game.status == GameStatus.PREPARATION:
            players = await self.app.store.game.get_players_by_game_id(game_id)

            if not players:
                await self.app.store.game.update_status_latest_game(
                    chat_id, GameStatus.FINISHED
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
                start_text += self.players_to_markdown(players, with_track=True)

                await self.app.store.tg_api.send_message(
                    Reply(
                        chat_id=chat_id,
                        text=start_text,
                        parse_mode="Markdown",
                    )
                )

                await self.app.store.tg_api.send_message(
                    await GameMessageHandler(self.app).start_game(
                        chat_id, game.id
                    )
                )
