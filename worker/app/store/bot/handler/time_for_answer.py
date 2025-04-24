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


class TimeForAnswerInlineHandler(BaseInlineButtonHandler):
    def __init__(self, app: "Application"):
        super().__init__(app)
        self.keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="10 секунд",
                        callback_data=InlineButtonType.ANSWER_TIME_10,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="20 секунд",
                        callback_data=InlineButtonType.ANSWER_TIME_20,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="30 секунд",
                        callback_data=InlineButtonType.ANSWER_TIME_30,
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

        text = "Выберите время на ответ"

        return Reply(
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=self.keyboard,
        )
