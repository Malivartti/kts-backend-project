import typing

from app.store.tg_api.dataclasses import CallbackUpdate, Reply, Update

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BaseHandler:
    def __init__(self, app: "Application"):
        self.app = app

    async def handle(self, update: Update | CallbackUpdate) -> Reply:
        raise NotImplementedError


class BaseCommandHandler:
    def __init__(self, app: "Application"):
        self.app = app

    async def handle(self, update: Update) -> Reply:
        raise NotImplementedError


class BaseInlineButtonHandler:
    def __init__(self, app: "Application"):
        self.app = app

    async def handle(self, update: CallbackUpdate) -> Reply:
        raise NotImplementedError
