from aiohttp.web_app import Application

__all__ = ("setup_routes",)


def setup_routes(application: Application):
    import app.quiz.routes
    import app.user.routes

    app.user.routes.register_urls(application)
    app.quiz.routes.register_urls(application)
