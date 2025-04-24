from app.game.accessor import UpdateGameSettings
from app.store.bot.handler.base_handler import BaseInlineButtonHandler
from app.store.bot.handler.shared import (
    get_minutes_to_text,
    get_seconds_to_text,
)
from app.store.bot.types import InlineButtonType
from app.store.tg_api.dataclasses import (
    CallbackUpdate,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Reply,
)


class SettingsInlineHandler(BaseInlineButtonHandler):
    async def _get_keyboard(self, chat_id: int):
        game = await self.app.store.game.get_latest_game(chat_id)

        theme_text = "Все темы"
        if game.theme_id:
            theme = await self.app.store.quiz.get_theme_by_id(game.theme_id)
            theme_text = theme.title

        game_time_text = "До выбывания"
        if game.time_for_game:
            game_time_text = f"{game.time_for_game} " + get_minutes_to_text(
                game.time_for_game
            )

        answer_time_text = f"{game.time_for_answer} " + get_seconds_to_text(
            game.time_for_answer
        )

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Тема: {theme_text}",
                        callback_data=InlineButtonType.SELECT_THEME,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=f"Время игры: {game_time_text}",
                        callback_data=InlineButtonType.TIME_FOR_GAME,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=f"Время ответа: {answer_time_text}",
                        callback_data=InlineButtonType.TIME_FOR_ANSWER,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Готово",
                        callback_data=InlineButtonType.SETTINGS_DONE,
                    ),
                ],
            ]
        )

    async def handle(self, update: CallbackUpdate) -> Reply:
        chat_id = update.callback_query.message.chat.id

        game = await self.app.store.game.get_latest_game(chat_id)

        if game.manager.tg_id != update.callback_query.sender.id:
            return None

        callback_data = update.callback_query.data

        if callback_data == InlineButtonType.SETTINGS_DONE:
            message_id = update.callback_query.message.message_id
            return self.app.store.bot_manager.play_handler.create_reply(
                chat_id, message_id, game
            )

        settings_update: UpdateGameSettings = {}

        if callback_data.startswith("theme_"):
            value = None
            if callback_data != InlineButtonType.THEME_ALL:
                value = int(callback_data.split("_")[1])
            settings_update["theme_id"] = value

        elif callback_data.startswith("answer_time_"):
            value = int(callback_data.split("_")[-1])
            settings_update["time_for_answer"] = value

        elif callback_data.startswith("game_time_"):
            value = None
            time_value = callback_data.split("_")[-1]
            if time_value != "unlimited":
                value = int(time_value)
            settings_update["time_for_game"] = value

        await self.app.store.game.update_settings_lates_game(
            chat_id, settings_update
        )

        keyboard = await self._get_keyboard(chat_id)

        text = "Настройки игры"

        return Reply(
            chat_id=chat_id,
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=keyboard,
        )
