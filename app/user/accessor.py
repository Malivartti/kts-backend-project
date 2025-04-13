import typing

from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class UserAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        self.app = app
