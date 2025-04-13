import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


__all__ = ("register_urls",)


def register_urls(app: "Application"):
    pass
