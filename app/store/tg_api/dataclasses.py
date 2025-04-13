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
class Reply:
    chat_id: int
    text: str