import typing

from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp_session import get_session

if typing.TYPE_CHECKING:
    from app.web.app import Request

SESSION_COOKIE_NAME = "sessionid"


class AuthRequiredMixin:
    async def check_auth(self, request: "Request") -> dict:
        session = await get_session(self.request)
        session_key = session.get(SESSION_COOKIE_NAME)
        if not session_key:
            raise HTTPUnauthorized(reason="Authentication required")

        session_data = await request.app.store.session.get_by_session_key(
            session_key
        )
        if session_data is None:
            raise HTTPUnauthorized(reason="Invalid or expired session")

        session_data["session_key"] = session_key
        return session_data
