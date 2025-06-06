import typing

from app.store.bot.handler.base_handler import (
    BaseCommandHandler,
    BaseInlineButtonHandler,
)
from app.store.bot.handler.cancel import CancelInlineHandler
from app.store.bot.handler.game import GameMessageHandler
from app.store.bot.handler.info import InfoCommandHandler
from app.store.bot.handler.play import PlayHandler
from app.store.bot.handler.rating import RatingInlineHandler
from app.store.bot.handler.registration import RegistraionHandler
from app.store.bot.handler.rules import RulesInlineHandler
from app.store.bot.handler.settings import SettingsInlineHandler
from app.store.bot.handler.start import StartHandler
from app.store.bot.handler.stop import StopCommandHandler
from app.store.bot.handler.theme import ThemeInlineHandler
from app.store.bot.handler.time_for_answer import (
    TimeForAnswerInlineHandler,
)
from app.store.bot.handler.time_for_game import TimeForGameInlineHandler
from app.store.bot.types import CommandType, InlineButtonType
from app.store.tg_api.dataclasses import CallbackUpdate, Reply, Update

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.start_handler = StartHandler(app)
        self.play_handler = PlayHandler(app)
        self.settings_handler = SettingsInlineHandler(app)
        self.game_message_handler = GameMessageHandler(app)

        self.inline_button_handlers: dict[
            InlineButtonType, BaseInlineButtonHandler
        ] = {
            InlineButtonType.HOME: self.start_handler,
            InlineButtonType.PLAY: self.play_handler,
            InlineButtonType.CANCEL: CancelInlineHandler(app),
            InlineButtonType.REGISTRATION: RegistraionHandler(app),
            InlineButtonType.RULES: RulesInlineHandler(app),
            InlineButtonType.RATING: RatingInlineHandler(app),
            InlineButtonType.SETTINGS: self.settings_handler,
            InlineButtonType.SETTINGS_DONE: self.settings_handler,
            InlineButtonType.SELECT_THEME: ThemeInlineHandler(app),
            InlineButtonType.TIME_FOR_ANSWER: TimeForAnswerInlineHandler(app),
            InlineButtonType.TIME_FOR_GAME: TimeForGameInlineHandler(app),
        }
        self.command_handlers: dict[InlineButtonType, BaseCommandHandler] = {
            CommandType.START: self.start_handler,
            CommandType.PLAY: self.play_handler,
            CommandType.STOP: StopCommandHandler(app),
            CommandType.INFO: InfoCommandHandler(app),
        }

    async def handle_updates(self, updates: list[Update | CallbackUpdate]):
        for update in updates:
            if isinstance(update, CallbackUpdate):
                await self.handle_inline_button(update)
            elif update.message.text.startswith("/"):
                await self.handle_command(update)
            else:
                await self.handle_message(update)

    async def handle_inline_button(self, update: CallbackUpdate):
        callback_data = update.callback_query.data

        if callback_data.startswith(("theme_", "answer_time_", "game_time_")):
            reply = await self.settings_handler.handle(update)
        else:
            handler = self.inline_button_handlers.get(callback_data)
            if not handler:
                return
            reply = await handler.handle(update)

        if not reply:
            return
        if reply.message_id:
            await self._edit_reply(reply)
        else:
            await self._send_reply(reply)

    async def handle_command(self, update: Update):
        text = update.message.text

        chat_id = update.message.chat.id
        if chat_id > 0 and text != CommandType.START:
            await self._send_reply(
                Reply(
                    chat_id=chat_id,
                    text=(
                        "Да, это моя команда, но она работает только "
                        "для группового чата. Если хотите играть "
                        "в одиночку, то все равно нужно создать "
                        "групповой чат, где будем мы с Вами."
                    ),
                )
            )
            return

        if "@" in text:
            command_parts = text.split("@", 1)
            if command_parts[1] != self.app.config.bot.tg_name:
                return
            text = command_parts[0]

        handler = self.command_handlers.get(text)
        if handler:
            reply = await handler.handle(update)
            await self._send_reply(reply)

    async def handle_message(self, update: Update):
        if update.message.sender.is_bot:
            return

        replies = await self.game_message_handler.handle(update)
        for reply in replies:
            await self._send_reply(reply)

    async def _send_reply(self, reply: Reply):
        await self.app.store.tg_api.send_message(reply)

    async def _edit_reply(self, reply: Reply):
        await self.app.store.tg_api.edit_message(reply)
