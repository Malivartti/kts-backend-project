from app.game.models import GameStatus
from app.store.bot.handler.base_handler import BaseCommandHandler
from app.store.tg_api.dataclasses import Reply, Update


class StopCommandHandler(BaseCommandHandler):
    async def handle(self, update: Update) -> Reply:
        chat_id = update.message.chat.id
        game = await self.app.store.game.get_latest_game(chat_id)

        if (
            game
            and game.status == GameStatus.ACTIVE
            or game.status == GameStatus.PREPARATION
        ):
            await self.app.store.game.update_status_latest_game(
                chat_id, GameStatus.FINISHED
            )
            reply = Reply(chat_id=update.message.chat.id, text="Игра завершена")
        elif not game or game.status == GameStatus.FINISHED:
            reply = Reply(
                chat_id=update.message.chat.id, text="Игра не запущена"
            )
        return reply
