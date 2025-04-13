import logging
import os
import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_logging(_: "Application") -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'logs'
    )
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info('Starting app')