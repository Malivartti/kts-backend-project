from dataclasses import dataclass


@dataclass
class Sender:
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None
    username: str | None


@dataclass
class Chat:
    id: int
    type: str


@dataclass
class Message:
    message_id: int
    sender: Sender
    chat: Chat
    date: int
    text: str


@dataclass
class Update:
    update_id: int
    message: Message


@dataclass
class InlineKeyboardButton:
    text: str
    callback_data: str


@dataclass
class InlineKeyboardMarkup:
    inline_keyboard: list[list[InlineKeyboardButton]]


@dataclass
class KeyboardButton:
    text: str
    request_contact: bool | None = None
    request_location: bool | None = None


@dataclass
class ReplyKeyboardMarkup:
    keyboard: list[list[KeyboardButton]] | None = None
    remove_keyboard: bool | None = None
    resize_keyboard: bool | None = None
    one_time_keyboard: bool | None = None
    selective: bool | None = None
    input_field_placeholder: str | None = None


@dataclass
class Reply:
    chat_id: int
    text: str
    reply_markup: InlineKeyboardMarkup | None = None
    message_id: int | None = None
    parse_mode: str | None = None


@dataclass
class CallbackQuery:
    id: int
    sender: Sender
    message: Message
    data: str


@dataclass
class CallbackUpdate:
    update_id: int
    callback_query: CallbackQuery
