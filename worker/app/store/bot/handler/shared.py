from app.game.models import Game, GamePlayer, TrackColor
from app.store.bot.types import InlineButtonType
from app.store.tg_api.dataclasses import (
    CallbackQuery,
    CallbackUpdate,
    Chat,
    Message,
    Sender,
)


def get_seconds_to_text(seconds: int) -> str:
    last_digit = seconds % 10
    last_two_digits = seconds % 100

    if last_two_digits in range(11, 20):
        word = "секунд"
    elif last_digit == 1:
        word = "секунда"
    elif last_digit in range(2, 5):
        word = "секунды"
    else:
        word = "секунд"
    return word


def get_minutes_to_text(minutes: int) -> str:
    last_digit = minutes % 10
    last_two_digits = minutes % 100

    if last_two_digits in range(11, 20):
        word = "минут"
    elif last_digit == 1:
        word = "минута"
    elif last_digit in range(2, 5):
        word = "минуты"
    else:
        word = "минут"
    return word


def time_for_reg_reg_text(seconds: int) -> str:
    word = get_seconds_to_text(seconds)
    return f"До конца регистрации осталось {seconds} {word}\n"


def time_for_game_reg_text(minutes: int | None) -> str:
    text = "Игра будет продолжаться "
    if minutes is None:
        text += "до выбывания участников"
    else:
        text += f"{minutes} {get_minutes_to_text(minutes)}"
    return text + "\n"


def time_for_answer_reg_text(seconds: int):
    word = get_seconds_to_text(seconds)
    return f"Время на ответ {seconds} {word}\n"


def game_reg_settings_text(game: Game) -> str:
    return (
        time_for_reg_reg_text(15)
        + time_for_game_reg_text(game.time_for_game)
        + time_for_answer_reg_text(game.time_for_answer)
    )


def time_for_reg_set_text(seconds: int) -> str:
    word = get_seconds_to_text(seconds)
    return f"Время на регистрацию:  {seconds} {word}\n"


def time_for_game_set_text(minutes: int | None) -> str:
    text = "Время игры: "
    if minutes is None:
        text += "До выбывания участников"
    else:
        text += f"{minutes} {get_minutes_to_text(minutes)}"
    return text + "\n"


def time_for_answer_set_text(seconds: int):
    word = get_seconds_to_text(seconds)
    return f"Время на ответ: {seconds} {word}\n"


def game_settings_text(game: Game) -> str:
    return (
        time_for_reg_set_text(15)
        + time_for_game_set_text(game.time_for_game)
        + time_for_answer_set_text(game.time_for_answer)
    )


track_emoji = {
    TrackColor.RED: "🔴",
    TrackColor.YELLOW: "🟡",
    TrackColor.GREEN: "🟢",
}


def player_to_md(player: GamePlayer) -> str:
    player_name = player.first_name
    if player.last_name:
        player_name += " " + player.last_name

    return f"[{player_name}](tg://user?id={player.tg_id})"


def players_to_md(
    players: list[GamePlayer], with_track: bool = False, is_rating: bool = False
) -> str:
    text = ""
    for player in players:
        line = ""
        player_md = player_to_md(player)

        if is_rating:
            line += f"{player.place} место: "

        line += player_md

        if is_rating:
            line += (
                f" (правильно {player.correct_answers}, "
                f"неправильно {player.incorrect_answers})"
            )

        if with_track:
            line += f" {track_emoji[player.track]}"

        text += f"\n{line}"
    return text


def create_callback(
    chat_id: int,
    message_id: int,
    sender: Sender,
    inline_btn: InlineButtonType,
) -> CallbackUpdate:
    return CallbackUpdate(
        update_id=0,
        callback_query=CallbackQuery(
            id=0,
            sender=sender,
            message=Message(
                message_id=message_id,
                sender=sender,
                chat=Chat(id=chat_id, type="group"),
                date=0,
                text="",
            ),
            data=inline_btn,
        ),
    )
