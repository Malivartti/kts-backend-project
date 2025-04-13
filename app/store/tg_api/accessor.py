import logging
import typing
from urllib.parse import urlencode

from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.tg_api.mappers import dict_to_update, reply_to_dict

from .dataclasses import Reply, Update
from .poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application

API_BASE_URL = "https://api.telegram.org"


class TgApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: ClientSession | None = None
        self.token: str | None = None
        self.poller: Poller | None = None
        self.offset: int | None = None

    async def connect(self, app: "Application"):
        self.token = app.config.bot.token
        self.session = ClientSession()
        self.poller = Poller(store=app.store)
        self.offset = None
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.poller:
            await self.poller.stop()
        if self.session:
            await self.session.close()

    def _build_query(self, method: str, params: dict) -> str:
        if params is None:
            params = {}
        return f"{API_BASE_URL}/bot{self.token}/{method}?{urlencode(params)}"

    async def poll(self) -> list[Update]:
        params = {"timeout": 25}
        if self.offset:
            params["offset"] = self.offset

        url = self._build_query("getUpdates", params)
        async with self.session.get(url) as response:
            data = await response.json()
            if not data.get("ok"):
                logging.error(
                    "Failed to get updates: %s", data.get("description")
                )
                return []

            updates = []
            for update in data.get("result", []):
                if "message" in update and "text" in update["message"]:
                    updates.append(dict_to_update(update))
                self.offset = max(self.offset or 0, update["update_id"] + 1)
            return updates

    async def send_message(self, reply: Reply) -> None:
        url = self._build_query("sendMessage", reply_to_dict(reply))
        async with self.session.get(url) as response:
            data = await response.json()
            if not data.get("ok"):
                logging.error(
                    "Failed to send message: %s", data.get("description")
                )
                return
