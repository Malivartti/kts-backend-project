from app.game.models import Game, GameStatus
from app.store.bot.handler.base_handler import BaseCommandHandler
from app.store.bot.handler.shared import players_to_md
from app.store.tg_api.dataclasses import Reply, Update


class InfoCommandHandler(BaseCommandHandler):
    async def handle(self, update: Update) -> Reply:
        chat_id = update.message.chat.id
        game = await self.app.store.game.get_latest_game(chat_id)
        if not game:
            return Reply(chat_id=chat_id, text="В этом чате ещё не было игр.")

        message = await self.create_text(game)

        return Reply(chat_id=chat_id, text=message, parse_mode="Markdown")

    async def create_text(self, game: Game, head: str | None = None) -> str:
        players = await self.app.store.game.get_players_by_game_id(game.id)

        message = ""

        if head:
            header = f"*{head}*"
        elif game.status == GameStatus.ACTIVE:
            header = "📊 *Информация о текущей игре*"
        else:
            header = "📊 *Информация о последней игре*"

        message = f"{header}"

        winners = sorted(
            [p for p in players if p.place is not None], key=lambda p: p.place
        )
        if winners:
            message += "\n\n*🏆 Победители:*"
            message += players_to_md(winners, with_track=True, is_rating=True)

        active_players = [p for p in players if p.in_game and p.place is None]
        if active_players:
            message += "\n\n*👥 Участники:*"
            message += players_to_md(active_players, with_track=True)

        eliminated_players = [
            p for p in players if not p.in_game and p.place is None
        ]
        if eliminated_players:
            message += "\n\n*❌ Выбывшие:*"
            message += players_to_md(eliminated_players, with_track=True)

        return message
