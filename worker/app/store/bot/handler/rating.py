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


class RatingInlineHandler(BaseInlineButtonHandler):
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

    async def handle(self, update: CallbackUpdate) -> Reply:
        rating_data = await self.app.store.game.get_rating()
        rating_text = self._format_rating_text(rating_data)

        return Reply(
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id,
            text=rating_text,
            reply_markup=self.keyboard,
        )

    def _format_rating_text(self, rating_data):
        if not rating_data:
            return "Рейтинг игроков:\n\nПока нет данных о завершенных играх."

        text = "🏆 Рейтинг игроков 🏆\n\n"

        for i, player in enumerate(rating_data, 1):
            player_name = player["first_name"]
            if player["last_name"]:
                player_name += f" {player['last_name']}"

            text += f"{i}. {player_name} — {player['points']} очков\n"

        text += "\nОчки начисляются за места:\n"
        text += "🥇 1 место — 5 очков\n"
        text += "🥈 2 место — 3 очка\n"
        text += "🥉 3 место — 1 очко"

        return text
