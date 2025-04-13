from aiohttp.web import (
    Application as AiohttpApplication,
)

from app.store.database.database import Database
from app.store.store import Store, setup_store
from app.web.config import Config, setup_config
from app.web.logger import setup_logging

from .routes import setup_routes

__all__ = ("Application",)


class Application(AiohttpApplication):
    config: Config = None
    store: Store = None
    database: Database = None


app = Application()


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    setup_routes(app)
    setup_store(app)
    return app
