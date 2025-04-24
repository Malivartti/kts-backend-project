from app.game.models import GameStatus
from app.store.bot.handler.base_handler import BaseInlineButtonHandler
from app.store.bot.handler.shared import create_callback
from app.store.bot.types import InlineButtonType
from app.store.tg_api.dataclasses import CallbackUpdate, Reply


class CancelInlineHandler(BaseInlineButtonHandler):
    async def handle(self, update: CallbackUpdate) -> Reply:
        chat_id = update.callback_query.message.chat.id
        user = update.callback_query.sender
        message_id = update.callback_query.message.message_id
        game = await self.app.store.game.get_latest_game(chat_id)

        if game.manager.tg_id != user.id:
            return None

        await self.app.store.game.update_status_latest_game(
            chat_id, GameStatus.CANCELED
        )

        callback_update = create_callback(
            chat_id, message_id, user, InlineButtonType.HOME
        )

        accessor = self.app.store.bot_manager
        return await accessor.start_handler.handle(callback_update)
