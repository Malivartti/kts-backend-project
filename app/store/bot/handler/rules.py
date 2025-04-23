from app.store.bot.handler.base_handler import BaseInlineButtonHandler
from app.store.bot.types import InlineButtonType
from app.store.tg_api.dataclasses import (
    CallbackUpdate,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Reply,
)


class RulesInlineHandler(BaseInlineButtonHandler):
    async def handle(self, update: CallbackUpdate) -> Reply:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Назад", callback_data=InlineButtonType.HOME
                    )
                ]
            ]
        )

        text = (
            "Основные принципы\n"
            '"Умники и умницы" — это интеллектуальная игра-викторина для '
            "групповых чатов, основанная на одноименной "
            "телепередаче. Игроки соревнуются, отвечая на вопросы и "
            "продвигаясь по игровым дорожкам разного цвета и сложности.\n\n"
            "Правила\n"
            "- В игре участвуют несколько игроков\n"
            "- Каждый игрок получает дорожку (красную, жёлтую или зелёную)\n"
            "- Игроки отвечают на вопросы и зарабатывают очки\n"
            "- Побеждает тот, кто первым достигнет конца дорожки\n\n"
            "Дорожки и их особенности\n"
            "В игре существует три типа дорожек, каждая со своими условиями:"
            "\n\n"
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

        return Reply(
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=keyboard,
        )
