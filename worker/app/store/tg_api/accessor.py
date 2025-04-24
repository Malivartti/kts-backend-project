import logging
import typing
from urllib.parse import urlencode

from aiohttp.client import ClientSession
from app.base.base_accessor import BaseAccessor
from app.store.tg_api.mappers import (
    reply_to_dict,
)

from .dataclasses import Reply

if typing.TYPE_CHECKING:
    from app.web.app import Application

API_BASE_URL = "https://api.telegram.org"


class TgApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: ClientSession | None = None
        self.token: str | None = None
        self.offset: int | None = None

    async def connect(self, app: "Application"):
        self.token = app.config.bot.token
        self.session = ClientSession()
        self.offset = None

    async def disconnect(self, app: "Application"):
        if self.session:
            await self.session.close()

    def _build_query(self, method: str, params: dict) -> str:
        if params is None:
            params = {}
        return f"{API_BASE_URL}/bot{self.token}/{method}?{urlencode(params)}"

    async def send_message(self, reply: Reply) -> None:
        d_reply = reply_to_dict(reply)
        d_reply["disable_notification"] = True
        url = self._build_query("sendMessage", d_reply)
        async with self.session.get(url) as response:
            data = await response.json()
            if not data.get("ok"):
                logging.error(
                    "Failed to send message: %s\nreply: %s",
                    data.get("description"),
                    d_reply,
                )
                return

    async def edit_message(self, reply: Reply) -> None:
        d_reply = reply_to_dict(reply)
        d_reply["disable_notification"] = True
        url = self._build_query("editMessageText", d_reply)
        async with self.session.get(url) as response:
            data = await response.json()
            if not data.get("ok"):
                logging.error(
                    "Failed to edit message: %s\nreply: %s",
                    data.get("description"),
                    d_reply,
                )
                return
