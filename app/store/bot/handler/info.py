from app.game.models import GamePlayer, GameStatus
from app.store.bot.handler.base_handler import BaseCommandHandler
from app.store.bot.types import track_emoji
from app.store.tg_api.dataclasses import Reply, Update


class InfoCommandHandler(BaseCommandHandler):
    async def handle(self, update: Update) -> Reply:
        chat_id = update.message.chat.id
        game = await self.app.store.game.get_latest_game(chat_id)
        if not game:
            return Reply(chat_id=chat_id, text="В этом чате ещё не было игр.")

        players = await self.app.store.game.get_players_by_game_id(game.id)

        if game.status == GameStatus.ACTIVE:
            header = "📊 *Информация о текущей игре*"
        else:
            header = "📊 *Информация о последней игре*"

        message = f"{header}\n"

        winners = sorted(
            [p for p in players if p.place is not None], key=lambda p: p.place
        )
        if winners:
            message += "\n*🏆 Победители:*\n"
            message += self.players_to_markdown(winners, is_rating=True)

        active_players = [p for p in players if p.in_game and p.place is None]
        if active_players:
            message += "\n*👥 Участники:*\n"
            message += self.players_to_markdown(active_players)

        eliminated_players = [
            p for p in players if not p.in_game and p.place is None
        ]
        if eliminated_players:
            message += "\n*❌ Выбывшие:*\n"
            message += self.players_to_markdown(eliminated_players)

        return Reply(chat_id=chat_id, text=message, parse_mode="Markdown")

    def players_to_markdown(
        self, players: list[GamePlayer], is_rating: bool = False
    ) -> str:
        text = ""
        for player in players:
            player_name = player.first_name
            if player.last_name:
                player_name += " " + player.last_name

            player_link = f"[{player_name}](tg://user?id={player.tg_id})"
            if is_rating:
                text += f"{player.place} место: "
            text += (
                f"{player_link} (правильно {player.correct_answers}, "
                f"неправильно {player.incorrect_answers}) "
                f"{track_emoji[player.track]}\n"
            )
        return text
