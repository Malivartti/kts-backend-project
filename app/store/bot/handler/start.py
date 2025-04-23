from app.store.bot.handler.base_handler import (
    BaseHandler,
)
from app.store.bot.types import InlineButtonType
from app.store.tg_api.dataclasses import (
    CallbackUpdate,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Reply,
    Update,
)


class StartHandler(BaseHandler):
    async def handle(self, update: Update | CallbackUpdate) -> Reply:
        if isinstance(update, Update):
            chat_id = update.message.chat.id
        else:
            chat_id = update.callback_query.message.chat.id

        buttons = []
        if chat_id <= 0:
            buttons.append(
                InlineKeyboardButton(
                    text="Играть", callback_data=InlineButtonType.PLAY
                )
            )
        buttons.extend(
            [
                InlineKeyboardButton(
                    text="Правила", callback_data=InlineButtonType.RULES
                ),
                InlineKeyboardButton(
                    text="Рейтинг", callback_data=InlineButtonType.RATING
                ),
            ]
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

        text = "Добро пожаловать в игру 'Умники и умницы'! Выберите действие:"

        if isinstance(update, Update):
            return Reply(
                chat_id=chat_id,
                text=text,
                reply_markup=keyboard,
            )
        return Reply(
            chat_id=chat_id,
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=keyboard,
        )
