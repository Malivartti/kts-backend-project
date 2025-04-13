import typing

from app.store.tg_api.dataclasses import Reply, Update

# from app.store.tg_api.dataclasses import Update, Message

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app

    async def handle_updates(self, updates: list[Update]):
       for update in updates:
            await self.app.store.tg_api.send_message(Reply(
                chat_id=update.message.chat.id,
                text=update.message.text
            ))