from app.store.bot.handler.base_handler import BaseInlineButtonHandler
from app.store.bot.types import InlineButtonType
from app.store.tg_api.dataclasses import (
    CallbackUpdate,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Reply,
)


class ThemeInlineHandler(BaseInlineButtonHandler):
    async def handle(self, update: CallbackUpdate) -> Reply:
        chat_id = update.callback_query.message.chat.id
        user_id = update.callback_query.sender.id
        game = await self.app.store.game.get_latest_game(chat_id)

        if game.manager.tg_id != user_id:
            return None

        themes = await self.app.store.quiz.get_themes()

        btns = [
            [
                InlineKeyboardButton(
                    text=theme.title, callback_data=f"theme_{theme.id}"
                ),
            ]
            for theme in themes
        ]
        btns.append(
            [
                InlineKeyboardButton(
                    text="Все темы", callback_data=InlineButtonType.THEME_ALL
                ),
            ]
        )

        self.keyboard = InlineKeyboardMarkup(inline_keyboard=btns)

        text = "Выберите тему"

        return Reply(
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=self.keyboard,
        )
