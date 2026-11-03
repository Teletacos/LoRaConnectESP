from classes.database.message import Message

class Chat:
    def __init__(self, chat_dicts):
        self.id = chat_dicts.get("id") or "chat_user1_user2"
        self.name = chat_dicts.get("name") or ""
        self.picture_name = chat_dicts.get("picture_name") or ""
        self.member_ids = chat_dicts.get("member_ids") or []
        self.created_at = chat_dicts.get("created_at") or "2026-10-20"
        message_list = chat_dicts.get("messages") or []
        self.messages = [Message(message) for message in message_list]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture_name": self.picture_name,
            "member_ids": self.member_ids,
            "created_at": self.created_at,
            "messages": [message.to_dict() for message in self.messages],
        }