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


class RulesInlineHandler(BaseInlineButtonHandler):
    def __init__(self, app: "Application"):
        super().__init__(app)
        self.keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Назад", callback_data=InlineButtonType.HOME
                    )
                ]
            ]
        )

        self.text = (
            "- В игре участвуют несколько игроков\n"
            "- Каждый игрок получает дорожку (красную, жёлтую или зелёную)\n"
            "- Игроки отвечают на вопросы и зарабатывают очки\n"
            "- Побеждает тот, кто первым достигнет конца дорожки\n\n"
            "В игре существует три типа дорожек, каждая со своими условиями:"
            "\n"
            "🔴 Красная дорожка\n"
            "Длина пути: 2 вопроса\n"
            "Допустимые ошибки: 0 (ни одной)\n\n"
            "🟡 Жёлтая дорожка\n"
            "Длина пути: 3 вопроса\n"
            "Допустимые ошибки: 1\n\n"
            "🟢 Зелёная дорожка\n"
            "Длина пути: 4 вопроса\n"
            "Допустимые ошибки: 2"
        )

    async def handle(self, update: CallbackUpdate) -> Reply:
        return Reply(
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id,
            text=self.text,
            reply_markup=self.keyboard,
        )
