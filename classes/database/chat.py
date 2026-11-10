from classes.database.message import Message

class Chat:
    def __init__(self, chat_dicts):
        self.id = chat_dicts.get("id") or 0
        self.name = chat_dicts.get("name") or ""
        self.member_ids = chat_dicts.get("member_ids") or []
        self.created_at = chat_dicts.get("created_at") or "2026-10-20"
        message_list = chat_dicts.get("messages") or []
        self.messages = [Message(message) for message in message_list]
        self._last_message = "Last message will be displayed here"
        self._member_picture_names = []

    def format_html(self, contacts):
        self._last_message = self.messages[-1].content
        self._member_picture_names.clear()
        for contact in contacts:
            if contact.id in self.member_ids:
                self._member_picture_names.append(contact.picture_name)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "member_ids": self.member_ids,
            "created_at": self.created_at,
            "messages": [message.to_dict() for message in self.messages],
        }