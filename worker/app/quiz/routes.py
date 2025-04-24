import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


__all__ = ("register_urls",)


def register_urls(app: "Application"):
    from app.quiz.views import (
        AnswerAddView,
        AnswerDeleteView,
        AnswerGetView,
        AnswerListView,
        AnswerUpdateView,
        QuestionAddView,
        QuestionDeleteView,
        QuestionGetView,
        QuestionListView,
        QuestionUpdateView,
        ThemeAddView,
        ThemeDeleteView,
        ThemeGetView,
        ThemeListView,
        ThemeUpdateView,
    )

    app.router.add_view("/quiz.add_theme", ThemeAddView)
    app.router.add_view("/quiz.update_theme", ThemeUpdateView)
    app.router.add_view("/quiz.delete_theme", ThemeDeleteView)
    app.router.add_view("/quiz.get_theme", ThemeGetView)
    app.router.add_view("/quiz.list_themes", ThemeListView)

    app.router.add_view("/quiz.add_question", QuestionAddView)
    app.router.add_view("/quiz.update_question", QuestionUpdateView)
    app.router.add_view("/quiz.delete_question", QuestionDeleteView)
    app.router.add_view("/quiz.get_questions", QuestionGetView)
    app.router.add_view("/quiz.list_questions", QuestionListView)

    app.router.add_view("/quiz.add_answer", AnswerAddView)
    app.router.add_view("/quiz.update_answer", AnswerUpdateView)
    app.router.add_view("/quiz.delete_answer", AnswerDeleteView)
    app.router.add_view("/quiz.get_answer", AnswerGetView)
    app.router.add_view("/quiz.list_answers", AnswerListView)
