

from app.store.tg_api.dataclasses import Chat, Message, Reply, Sender, Update


def dict_to_update(data: dict) -> Update:
    sender_data = data["message"]["from"]
    sender = Sender(
        id=sender_data["id"],
        is_bot=sender_data["is_bot"],
        first_name=sender_data["first_name"],
        last_name=sender_data.get("last_name"),
        username=sender_data.get("username")
    )
    
    chat_data = data["message"]["chat"]
    chat = Chat(
        id=chat_data["id"],
        type=chat_data["type"]
    )
    
    message_data = data["message"]
    message = Message(
        message_id=message_data["message_id"],
        sender=sender,
        chat=chat,
        date=message_data["date"],
        text=message_data["text"]
    )
    
    return Update(
        update_id=data["update_id"],
        message=message
    )


def reply_to_dict(reply: Reply) -> dict:
    return {
        "chat_id": reply.chat_id,
        "text": reply.text,
    }
