from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound
from aiohttp_apispec import (
    docs,
    querystring_schema,
    request_schema,
    response_schema,
)
from app.quiz.accessor import (
    AnswerUpdateFields,
    QuestionFilters,
    QuestionUpdateFields,
)
from app.quiz.models import (
    QuestionType,
    answer_to_dict,
    question_to_dict,
    theme_to_dict,
)
from app.quiz.schemes import (
    AnswerListResponseSchema,
    AnswerResponseSchema,
    AnswerSchema,
    AnswerSingleQuerySchema,
    AnswerUpdateSchema,
    OptionalQuestionSchema,
    QuestionAddSchema,
    QuestionListResponseSchema,
    QuestionResponseSchema,
    QuestionSingleQuerySchema,
    QuestionUpdateSchema,
    ThemeListResponseSchema,
    ThemeResponseSchema,
    ThemeSchema,
    ThemeSingleQuerySchema,
    ThemeUpdateSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @docs(tags=["themes"], summary="Add new theme")
    @request_schema(ThemeSchema)
    @response_schema(ThemeResponseSchema)
    async def post(self):
        await self.check_auth(self.request)

        data = self.request["data"]
        title = data["title"]

        quiz_accessor = self.request.app.store.quiz
        existing_theme = await quiz_accessor.get_theme_by_title(title)
        if existing_theme:
            raise HTTPConflict(reason="Theme with this title already exists")

        theme = await quiz_accessor.create_theme(title)
        return json_response(http_status=201, data=theme_to_dict(theme))


class ThemeUpdateView(AuthRequiredMixin, View):
    @docs(tags=["themes"], summary="Update theme by id")
    @querystring_schema(ThemeSingleQuerySchema)
    @request_schema(ThemeUpdateSchema)
    @response_schema(ThemeResponseSchema)
    async def put(self):
        await self.check_auth(self.request)

        theme_id = self.request["querystring"]["theme_id"]
        data = self.request["data"]
        title = data.get("title")

        quiz_accessor = self.request.app.store.quiz
        theme = await quiz_accessor.get_theme_by_id(theme_id)
        if not theme:
            raise HTTPNotFound(reason=f"Theme with id {theme_id} not found")

        if title and title != theme.title:
            existing = await quiz_accessor.get_theme_by_title(title)
            if existing:
                raise HTTPConflict(
                    reason="Theme with this title already exists"
                )

            theme = await quiz_accessor.update_theme(theme_id, title)

        return json_response(data=theme_to_dict(theme))


class ThemeDeleteView(AuthRequiredMixin, View):
    @docs(tags=["themes"], summary="Delete theme by id")
    @querystring_schema(ThemeSingleQuerySchema)
    @response_schema(OkResponseSchema)
    async def delete(self):
        await self.check_auth(self.request)

        theme_id = self.request["querystring"]["theme_id"]

        is_deleted = await self.request.app.store.quiz.delete_theme_by_id(
            theme_id
        )
        if not is_deleted:
            raise HTTPNotFound(reason=f"Theme with id {theme_id} not found")

        return json_response()


class ThemeGetView(View):
    @docs(tags=["themes"], summary="Get theme by id")
    @querystring_schema(ThemeSingleQuerySchema)
    @response_schema(ThemeResponseSchema)
    async def get(self):
        theme_id = self.request["querystring"]["theme_id"]
        theme = await self.request.app.store.quiz.get_theme_by_id(theme_id)
        if not theme:
            raise HTTPNotFound(reason=f"Theme with id {theme_id} not found")
        return json_response(data=theme_to_dict(theme))


class ThemeListView(View):
    @docs(tags=["themes"], summary="Get all themes")
    @response_schema(ThemeListResponseSchema)
    async def get(self):
        themes = await self.request.app.store.quiz.get_themes()
        return json_response(
            data={"themes": [theme_to_dict(theme) for theme in themes]}
        )


class QuestionAddView(AuthRequiredMixin, View):
    @docs(tags=["questions"], summary="Add new question")
    @request_schema(QuestionAddSchema)
    @response_schema(QuestionResponseSchema)
    async def post(self):
        session_data = await self.check_auth(self.request)
        user_id = session_data["user_id"]

        data = self.request["data"]
        title = data["title"]
        theme_id = data.get("theme_id")
        question_type = QuestionType(data["type"])

        quiz_accessor = self.request.app.store.quiz

        if theme_id is not None:
            theme = await quiz_accessor.get_theme_by_id(theme_id)
            if not theme:
                raise HTTPNotFound(reason=f"Theme with id {theme_id} not found")

        question = await quiz_accessor.create_question(
            user_id, title, question_type, theme_id
        )

        return json_response(
            http_status=201,
            data={
                "id": question.id,
                "title": question.title,
                "theme_id": question.theme_id,
                "type": question.type.value,
            },
        )


class QuestionUpdateView(AuthRequiredMixin, View):
    @docs(tags=["questions"], summary="Update question by id")
    @querystring_schema(QuestionSingleQuerySchema)
    @request_schema(QuestionUpdateSchema)
    @response_schema(QuestionResponseSchema)
    async def put(self):
        await self.check_auth(self.request)

        question_id = self.request["querystring"]["question_id"]
        data = self.request["data"]
        theme_id = data.get("theme_id")

        quiz_accessor = self.request.app.store.quiz
        question = await quiz_accessor.get_question_by_id(question_id)
        if not question:
            raise HTTPNotFound(
                reason=f"Question with id {question_id} not found"
            )

        if (
            "theme_id" in data
            and theme_id != question.theme_id
            and theme_id is not None
        ):
            existing = await quiz_accessor.get_theme_by_id(theme_id)
            if not existing:
                raise HTTPConflict(reason=f"Theme with id {theme_id} not found")

        update_fields: QuestionUpdateFields = {}
        for key, value in data.items():
            update_fields[key] = value

        question = await quiz_accessor.update_question(
            question_id, update_fields
        )
        return json_response(data=question_to_dict(question))


class QuestionDeleteView(AuthRequiredMixin, View):
    @docs(tags=["questions"], summary="Delete question by id")
    @querystring_schema(QuestionSingleQuerySchema)
    @response_schema(OkResponseSchema)
    async def delete(self):
        await self.check_auth(self.request)

        question_id = self.request["querystring"]["question_id"]

        is_deleted = await self.request.app.store.quiz.delete_question_by_id(
            question_id
        )
        if not is_deleted:
            raise HTTPNotFound(
                reason=f"Question with id {question_id} not found"
            )

        return json_response()


class QuestionGetView(View):
    @docs(tags=["questions"], summary="Get question by id")
    @querystring_schema(QuestionSingleQuerySchema)
    @response_schema(QuestionResponseSchema)
    async def get(self):
        question_id = self.request["querystring"]["question_id"]
        question = await self.request.app.store.quiz.get_question_by_id(
            question_id
        )
        if not question:
            raise HTTPNotFound(reason=f"Theme with id {question_id} not found")
        return json_response(data=question_to_dict(question))


class QuestionListView(View):
    @docs(tags=["questions"], summary="Get all questions")
    @querystring_schema(OptionalQuestionSchema)
    @response_schema(QuestionListResponseSchema)
    async def get(self):
        filters: QuestionFilters = {}
        for key, value in self.request["querystring"].items():
            filters[key] = value

        quiz_accessor = self.request.app.store.quiz

        questions = await quiz_accessor.get_questions(filters)

        return json_response(
            data={
                "questions": [
                    question_to_dict(question) for question in questions
                ]
            }
        )


class AnswerAddView(AuthRequiredMixin, View):
    @docs(tags=["answers"], summary="Add new answer")
    @request_schema(AnswerSchema)
    @response_schema(AnswerResponseSchema)
    async def post(self):
        await self.check_auth(self.request)

        data = self.request["data"]
        question_id = data["question_id"]
        title = data["title"]
        is_correct = data["is_correct"]

        quiz_accessor = self.request.app.store.quiz
        question = await quiz_accessor.get_question_by_id(question_id)
        if not question:
            raise HTTPNotFound(
                reason=f"Question with id {question_id} not found"
            )

        answer = await quiz_accessor.create_answer(
            question_id, title, is_correct
        )

        return json_response(http_status=201, data=answer_to_dict(answer))


class AnswerUpdateView(AuthRequiredMixin, View):
    @docs(tags=["answers"], summary="Update answer by id")
    @querystring_schema(AnswerSingleQuerySchema)
    @request_schema(AnswerUpdateSchema)
    @response_schema(AnswerResponseSchema)
    async def put(self):
        await self.check_auth(self.request)

        answer_id = self.request["querystring"]["answer_id"]
        data = self.request["data"]

        quiz_accessor = self.request.app.store.quiz
        answer = await quiz_accessor.get_answer_by_id(answer_id)
        if not answer:
            raise HTTPNotFound(reason=f"Answer with id {answer_id} not found")

        update_fields: AnswerUpdateFields = {}
        for key, value in data.items():
            update_fields[key] = value

        updated_answer = await quiz_accessor.update_answer(
            answer_id, update_fields
        )
        return json_response(data=answer_to_dict(updated_answer))


class AnswerDeleteView(AuthRequiredMixin, View):
    @docs(tags=["answers"], summary="Delete answer by id")
    @querystring_schema(AnswerSingleQuerySchema)
    @response_schema(OkResponseSchema)
    async def delete(self):
        await self.check_auth(self.request)

        answer_id = self.request["querystring"]["answer_id"]

        quiz_accessor = self.request.app.store.quiz
        is_deleted = await quiz_accessor.delete_answer(answer_id)
        if not is_deleted:
            raise HTTPNotFound(reason=f"Answer with id {answer_id} not found")

        return json_response()


class AnswerGetView(View):
    @docs(tags=["answers"], summary="Get answer by id")
    @querystring_schema(AnswerSingleQuerySchema)
    @response_schema(AnswerResponseSchema)
    async def get(self):
        answer_id = self.request["querystring"]["answer_id"]
        answer = await self.request.app.store.quiz.get_answer_by_id(answer_id)

        if not answer:
            raise HTTPNotFound(reason=f"Answer with id {answer_id} not found")

        return json_response(data=answer_to_dict(answer))


class AnswerListView(View):
    @docs(tags=["answers"], summary="Get answers by question")
    @response_schema(AnswerListResponseSchema)
    async def get(self):
        answers = await self.request.app.store.quiz.get_answers()

        return json_response(
            data={"answers": [answer_to_dict(answer) for answer in answers]}
        )
