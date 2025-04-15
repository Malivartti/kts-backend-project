import base64
import json
import uuid
from datetime import datetime, timedelta

from sqlalchemy import select

from app.base.base_accessor import BaseAccessor
from app.session.models import Session

SESSION_DURATION = timedelta(days=1)


class SessionAccessor(BaseAccessor):
    async def create_session(self, user_id: int) -> str:
        session_key = str(uuid.uuid4())
        session_data = base64.b64encode(
            json.dumps({"user_id": user_id}).encode("utf-8")
        ).decode("utf-8")
        expire_date = datetime.now() + SESSION_DURATION

        session_data = Session(
            session_key=session_key,
            session_data=session_data,
            expire_date=expire_date,
        )

        async with self.app.database.session() as session:
            session.add(session_data)
            await session.commit()
        return session_key

    async def get_by_session_key(self, session_key: str) -> dict | None:
        async with self.app.database.session() as session:
            query = select(Session).where(
                Session.session_key == session_key,
                Session.expire_date > datetime.now(),
            )
            result = await session.execute(query)
            session_data = result.scalar_one_or_none()
            if session_data:
                return json.loads(
                    base64.b64decode(
                        session_data.session_data.encode("utf-8")
                    ).decode("utf-8")
                )
            return None

    async def delete_session(self, session_key: str) -> None:
        async with self.app.database.session() as session:
            query = select(Session).where(Session.session_key == session_key)
            result = await session.execute(query)
            session_data = result.scalar_one_or_none()
            if session_data:
                await session.delete(session_data)
                await session.commit()
