from typing import TYPE_CHECKING, NotRequired, TypedDict

from sqlalchemy import and_, select, update

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Answer, Question, QuestionType, Theme

if TYPE_CHECKING:
    from app.web.app import Application


class QuestionUpdateFields(TypedDict, total=False):
    title: NotRequired[str]
    theme_id: NotRequired[int | None]
    type: NotRequired[QuestionType]


class QuestionFilters(TypedDict, total=False):
    id: NotRequired[int]
    user_id: NotRequired[int]
    theme_id: NotRequired[int | None]
    type: NotRequired[QuestionType]
    title: NotRequired[str]


class AnswerUpdateFields(TypedDict, total=False):
    title: NotRequired[str]
    is_correct: NotRequired[bool]


class QuizAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        self.app = app

    async def create_theme(self, title: str) -> Theme:
        theme = Theme(title=title)
        async with self.app.database.session() as session:
            session.add(theme)
            await session.commit()
            await session.refresh(theme)
        return theme

    async def update_theme(self, theme_id: int, new_title: str) -> Theme | None:
        async with self.app.database.session() as session:
            existing = await session.get(Theme, theme_id)
            if not existing:
                return None

            await session.execute(
                update(Theme)
                .where(Theme.id == theme_id)
                .values(title=new_title)
            )

            await session.refresh(existing)
            await session.commit()
            return existing

    async def delete_theme_by_id(self, theme_id: int) -> bool:
        async with self.app.database.session() as session:
            theme = await session.get(Theme, theme_id)
            if not theme:
                return False

            await session.delete(theme)
            await session.commit()
            return True

    async def get_theme_by_id(self, theme_id: int) -> Theme | None:
        async with self.app.database.session() as session:
            query = select(Theme).where(Theme.id == theme_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_theme_by_title(self, theme_title: str) -> Theme | None:
        async with self.app.database.session() as session:
            query = select(Theme).where(Theme.title == theme_title)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_themes(self) -> list[Theme]:
        async with self.app.database.session() as session:
            query = select(Theme)
            result = await session.execute(query)
            return list(result.scalars().all())

    async def create_question(
        self,
        user_id: int,
        title: str,
        question_type: QuestionType,
        theme_id: int | None = None,
    ) -> Question:
        question = Question(
            user_id=user_id, theme_id=theme_id, title=title, type=question_type
        )

        async with self.app.database.session() as session:
            session.add(question)
            await session.commit()
            await session.refresh(question)
        return question

    async def update_question(
        self, question_id: int, fields: QuestionUpdateFields
    ) -> Question | None:
        async with self.app.database.session() as session:
            question = await session.get(Question, question_id)
            if not question:
                return None

            await session.execute(
                update(Question)
                .where(Question.id == question_id)
                .values(**fields)
            )
            await session.commit()
            await session.refresh(question)
            return question

    async def delete_question_by_id(self, question_id: int) -> bool:
        async with self.app.database.session() as session:
            question = await session.get(Question, question_id)
            if not question:
                return False

            await session.delete(question)
            await session.commit()
            return True

    async def get_question_by_id(self, question_id: str) -> Question | None:
        async with self.app.database.session() as session:
            query = select(Question).where(Question.id == question_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_questions(
        self, filters: QuestionFilters | None = None
    ) -> list[Question]:
        query = select(Question)

        if filters:
            conditions = []

            if "user_id" in filters:
                conditions.append(Question.user_id == filters["user_id"])

            if "theme_id" in filters:
                conditions.append(Question.theme_id == filters["theme_id"])

            if "type" in filters:
                conditions.append(Question.type == filters["type"])

            if "title" in filters:
                search_term = f"%{filters['title']}%"
                conditions.append(Question.title.ilike(search_term))

            if conditions:
                query = query.where(and_(*conditions))

        async with self.app.database.session() as session:
            result = await session.execute(query)
            return list(result.scalars().all())

    async def create_answer(
        self, question_id: int, title: str, is_correct: bool
    ) -> Answer:
        answer = Answer(
            question_id=question_id, title=title, is_correct=is_correct
        )

        async with self.app.database.session() as session:
            session.add(answer)
            await session.commit()
            await session.refresh(answer)
        return answer

    async def update_answer(
        self, answer_id: int, fields: AnswerUpdateFields
    ) -> Answer | None:
        if not fields:
            return await self.get_by_id(answer_id)

        async with self.app.database.session() as session:
            answer = await session.get(Answer, answer_id)
            if not answer:
                return None

            await session.execute(
                update(Answer).where(Answer.id == answer_id).values(**fields)
            )
            await session.commit()
            await session.refresh(answer)
            return answer

    async def delete_answer(self, answer_id: int) -> bool:
        async with self.app.database.session() as session:
            answer = await session.get(Answer, answer_id)
            if not answer:
                return False

            await session.delete(answer)
            await session.commit()
            return True

    async def get_answer_by_id(self, answer_id: int) -> Answer | None:
        async with self.app.database.session() as session:
            query = select(Answer).where(Answer.id == answer_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_answers(self) -> list[Answer]:
        async with self.app.database.session() as session:
            query = select(Answer)
            result = await session.execute(query)
            return list(result.scalars().all())

    async def get_answers_by_question_id(
        self, question_id: int
    ) -> list[Answer]:
        async with self.app.database.session() as session:
            query = select(Answer).where(Answer.question_id == question_id)
            result = await session.execute(query)
            return list(result.scalars().all())

    async def get_correct_answer_by_question_id(
        self, question_id: int
    ) -> str | None:
        async with self.app.database.session() as session:
            query = select(Answer.title).where(
                Answer.question_id == question_id, Answer.is_correct.is_(True)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
