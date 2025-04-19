from aiohttp.web_exceptions import HTTPConflict, HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp_session import get_session, new_session

from app.user.schema import UserAuthSchema, UserResponseSchema
from app.web.app import View
from app.web.mixins import SESSION_COOKIE_NAME, AuthRequiredMixin
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response


async def login_user_and_set_session(request, user):
    session_key = await request.app.store.session.create_session(user.id)
    session = await new_session(request)
    session[SESSION_COOKIE_NAME] = session_key
    return json_response(data={"id": user.id, "username": user.username})


class UserRegisterView(View):
    @docs(tags=["user"], summary="User register")
    @request_schema(UserAuthSchema)
    @response_schema(UserResponseSchema)
    async def post(self):
        data = self.request["data"]
        username = data["username"]
        password = data["password"]

        user_accessor = self.request.app.store.user
        existing_user = await user_accessor.get_by_username(username)
        if existing_user:
            raise HTTPConflict(reason="Username already exists")

        user = await user_accessor.create_user(
            username=username, password=password
        )

        return await login_user_and_set_session(self.request, user)


class UserLoginView(View):
    @docs(tags=["user"], summary="User login")
    @request_schema(UserAuthSchema)
    @response_schema(UserResponseSchema)
    async def post(self):
        data = self.request["data"]
        username = data["username"]
        password = data["password"]

        user = await self.request.app.store.user.get_by_username(username)
        if not user:
            raise HTTPForbidden(reason="Invalid username or password")

        if not self.request.app.store.user.verify_password(
            password, user.password
        ):
            raise HTTPForbidden(reason="Invalid username or password")

        return await login_user_and_set_session(self.request, user)


class UserLogoutView(AuthRequiredMixin, View):
    @docs(tags=["user"], summary="Logout user")
    @response_schema(OkResponseSchema)
    async def get(self):
        session_data = await self.check_auth(self.request)

        session_key = session_data["session_key"]
        await self.request.app.store.session.delete_session(session_key)

        session = await get_session(self.request)
        del session[SESSION_COOKIE_NAME]

        return json_response(data={"status": "ok"})


class UserCurrentView(AuthRequiredMixin, View):
    @docs(tags=["user"], summary="Current user")
    @response_schema(UserResponseSchema)
    async def get(self):
        session_data = await self.check_auth(self.request)
        user = await self.request.app.store.user.get_by_id(
            session_data["user_id"]
        )

        return json_response(data={"id": user.id, "username": user.username})
