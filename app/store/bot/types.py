from app.base.types import BaseEnum
from app.game.models import TrackColor


class InlineButtonType(BaseEnum):
    HOME = "home"
    PLAY = "play"
    PLAY_SETTINGS = "play_settings"
    SETTINGS_TIME_TO_PLAY = "settings_time_to_play"
    SETTINGS_TIME_TO_REPLY = "settings_time_to_reply"
    PLAY_PARTICIPATE = "play_participate"
    RULES = "rules"
    RATING = "rating"
    LOCAL_RATING = "local_rating"
    GLOBAL_RATING = "global_rating"


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

track_emoji = {
    TrackColor.RED: "🔴",
    TrackColor.YELLOW: "🟡",
    TrackColor.GREEN: "🟢",
}
