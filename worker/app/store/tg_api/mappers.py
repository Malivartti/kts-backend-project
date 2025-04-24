from app.store.tg_api.dataclasses import (
    CallbackQuery,
    CallbackUpdate,
    Chat,
    InlineKeyboardMarkup,
    Message,
    Reply,
    ReplyKeyboardMarkup,
    Sender,
    Update,
)
from app.utils.string import enconde_dict_to_str


def dict_to_update(data: dict) -> Update:
    sender_data = data["message"]["from"]
    sender = Sender(
        id=sender_data["id"],
        is_bot=sender_data["is_bot"],
        first_name=sender_data["first_name"],
        last_name=sender_data.get("last_name"),
        username=sender_data.get("username"),
    )

    chat_data = data["message"]["chat"]
    chat = Chat(id=chat_data["id"], type=chat_data["type"])

    message_data = data["message"]
    message = Message(
        message_id=message_data["message_id"],
        sender=sender,
        chat=chat,
        date=message_data["date"],
        text=message_data["text"],
    )

    return Update(update_id=data["update_id"], message=message)


def markup_to_dict(markup: InlineKeyboardMarkup | ReplyKeyboardMarkup) -> dict:
    if isinstance(markup, InlineKeyboardMarkup):
        return {
            "inline_keyboard": [
                [
                    {"text": btn.text, "callback_data": btn.callback_data}
                    for btn in row
                ]
                for row in markup.inline_keyboard
            ]
        }

    result = {}

    if markup.keyboard is not None:
        result["keyboard"] = [
            [{"text": btn.text} for btn in row] for row in markup.keyboard
        ]

    if markup.remove_keyboard is not None:
        result["remove_keyboard"] = markup.remove_keyboard

    if markup.resize_keyboard is not None:
        result["resize_keyboard"] = markup.resize_keyboard

    if markup.one_time_keyboard is not None:
        result["one_time_keyboard"] = markup.one_time_keyboard

    if markup.selective is not None:
        result["selective"] = markup.selective

    if markup.input_field_placeholder is not None:
        result["input_field_placeholder"] = markup.input_field_placeholder

    return result


def reply_to_dict(reply: Reply) -> dict:
    params = {
        "chat_id": reply.chat_id,
        "text": reply.text,
    }

    if reply.reply_markup is not None:
        params["reply_markup"] = enconde_dict_to_str(
            markup_to_dict(reply.reply_markup)
        )

    if reply.message_id is not None:
        params["message_id"] = reply.message_id

    if reply.parse_mode is not None:
        params["parse_mode"] = reply.parse_mode

    return params


def dict_to_callback_update(data: dict) -> CallbackUpdate:
    message_data = data["callback_query"]["message"]

    chat_data = message_data["chat"]
    chat = Chat(id=chat_data["id"], type=chat_data["type"])

    message = Message(
        message_id=message_data["message_id"],
        sender=None,
        chat=chat,
        date=message_data["date"],
        text=message_data["text"],
    )

    sender_data = data["callback_query"]["from"]
    sender = Sender(
        id=sender_data["id"],
        is_bot=sender_data["is_bot"],
        first_name=sender_data["first_name"],
        last_name=sender_data.get("last_name"),
        username=sender_data.get("username"),
    )

    callback_query_data = data["callback_query"]
    callback_query = CallbackQuery(
        id=callback_query_data["id"],
        sender=sender,
        message=message,
        data=callback_query_data["data"],
    )

    return CallbackUpdate(
        update_id=data["update_id"], callback_query=callback_query
    )
