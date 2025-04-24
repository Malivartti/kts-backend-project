import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


__all__ = ("register_urls",)


def register_urls(app: "Application"):
    from app.user.views import (
        UserCurrentView,
        UserLoginView,
        UserLogoutView,
        UserRegisterView,
    )

    app.router.add_view("/user.register", UserRegisterView)
    app.router.add_view("/user.login", UserLoginView)
    app.router.add_view("/user.logout", UserLogoutView)
    app.router.add_view("/user.current", UserCurrentView)
