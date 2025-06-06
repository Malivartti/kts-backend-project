import typing

from app.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.game.accessor import GameAccessor
        from app.quiz.accessor import QuizAccessor
        from app.session.accessor import SessionAccessor
        from app.store.bot.manager import BotManager
        from app.store.queue.accessor import QueueAccessor
        from app.store.tg_api.accessor import TgApiAccessor
        from app.user.accessor import UserAccessor

        self.user = UserAccessor(app)
        self.quiz = QuizAccessor(app)
        self.game = GameAccessor(app)
        self.tg_api = TgApiAccessor(app)
        self.bot_manager = BotManager(app)
        self.session = SessionAccessor(app)
        self.queue = QueueAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
