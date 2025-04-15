import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "project"


@dataclass
class BotConfig:
    token: str


@dataclass
class SessionConfig:
    key: str


@dataclass
class Config:
    database: DatabaseConfig = None
    bot: BotConfig = None
    session: SessionConfig = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        database=DatabaseConfig(**raw_config["database"]),
        bot=BotConfig(
            token=raw_config["bot"]["token"],
        ),
        session=SessionConfig(key=raw_config["session"]["key"]),
    )
