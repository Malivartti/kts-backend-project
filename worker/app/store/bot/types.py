from app.base.types import BaseEnum
from app.game.models import TrackColor


class InlineButtonType(BaseEnum):
    HOME = "home"
    PLAY = "play"
    RULES = "rules"
    RATING = "rating"

    REGISTRATION = "registraion"
    CANCEL = "cancel"

    SETTINGS = "settings"
    SETTINGS_DONE = "settings_done"
    SELECT_THEME = "select_theme"
    TIME_FOR_ANSWER = "time_for_answer"
    TIME_FOR_GAME = "time_for_game"

    THEME_SPECIFIC = "theme_{id}"
    THEME_ALL = "theme_all"

    ANSWER_TIME_10 = "answer_time_10"
    ANSWER_TIME_20 = "answer_time_20"
    ANSWER_TIME_30 = "answer_time_30"

    GAME_TIME_1 = "game_time_1"
    GAME_TIME_2 = "game_time_2"
    GAME_TIME_5 = "game_time_5"
    GAME_TIME_UNLIMITED = "game_time_unlimited"


class CommandType(BaseEnum):
    START = "/start"
    PLAY = "/play"
    STOP = "/stop"
    INFO = "/info"


track_conditions = {
    TrackColor.RED: {
        "distance": 2,
        "mistakes": 0,
    },
    TrackColor.YELLOW: {
        "distance": 3,
        "mistakes": 1,
    },
    TrackColor.GREEN: {
        "distance": 4,
        "mistakes": 2,
    },
}
