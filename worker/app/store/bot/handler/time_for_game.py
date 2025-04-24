from typing import TYPE_CHECKING

from app.store.bot.handler.base_handler import BaseInlineButtonHandler
from app.store.bot.types import InlineButtonType
from app.store.tg_api.dataclasses import (
    CallbackUpdate,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Reply,
)

if TYPE_CHECKING:
    from app.web.app import Application


class TimeForGameInlineHandler(BaseInlineButtonHandler):
    def __init__(self, app: "Application"):
        super().__init__(app)
        self.keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="1 минута",
                        callback_data=InlineButtonType.GAME_TIME_1,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="2 минуты",
                        callback_data=InlineButtonType.GAME_TIME_2,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="5 минут",
                        callback_data=InlineButtonType.GAME_TIME_5,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="До выбывания",
                        callback_data=InlineButtonType.GAME_TIME_UNLIMITED,
                    ),
                ],
            ]
        )

    async def handle(self, update: CallbackUpdate) -> Reply:
        chat_id = update.callback_query.message.chat.id
        user_id = update.callback_query.sender.id
        game = await self.app.store.game.get_latest_game(chat_id)

        if game.manager.tg_id != user_id:
            return None

        text = "Выберите продолжительность игры"

        return Reply(
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=self.keyboard,
        )
