from app.game.models import GameStatus
from app.store.bot.handler.base_handler import BaseCommandHandler
from app.store.bot.handler.shared import player_to_md
from app.store.tg_api.dataclasses import Reply, Update


class StopCommandHandler(BaseCommandHandler):
    async def handle(self, update: Update) -> Reply:
        chat_id = update.message.chat.id
        game = await self.app.store.game.get_latest_game(chat_id)

        if game and game.status != GameStatus.FINISHED:
            if game.manager.tg_id == update.message.sender.id:
                await self.app.store.game.update_status_latest_game(
                    chat_id, GameStatus.FINISHED
                )
                return Reply(
                    chat_id=update.message.chat.id, text="Игра завершена"
                )

            return Reply(
                chat_id=update.message.chat.id,
                text=(
                    "Закончить игру может только ее создатель: "
                    + player_to_md(game.manager)
                ),
                parse_mode="Markdown",
            )

        return Reply(chat_id=update.message.chat.id, text="Игра не запущена")
