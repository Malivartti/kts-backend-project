import logging
import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_logging(_: "Application") -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    logger.handlers.clear()

    logger.addHandler(console_handler)

    logging.info("Starting app")
