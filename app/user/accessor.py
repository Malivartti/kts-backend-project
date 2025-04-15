import typing

from passlib.hash import pbkdf2_sha256
from sqlalchemy import select

from app.base.base_accessor import BaseAccessor
from app.user.models import User

if typing.TYPE_CHECKING:
    from app.web.app import Application


class UserAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        self.app = app

    def hash_password(self, password: str) -> str:
        return pbkdf2_sha256.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        return pbkdf2_sha256.verify(password, hashed)

    async def get_by_id(self, user_id: str) -> User | None:
        async with self.app.database.session() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        async with self.app.database.session() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create_user(
        self, username: str, password: str, is_admin: bool = False
    ) -> User:
        hashed_password = self.hash_password(password)
        user = User(
            username=username, password=hashed_password, is_admin=is_admin
        )

        async with self.app.database.session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user
