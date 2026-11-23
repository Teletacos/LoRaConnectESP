from classes.database.message import Message
from urandom import getrandbits

class Chat:
    def __init__(self, chat_dict=None, id=None, name=None, member_ids=[], messages=[]):
        if chat_dict:
            self.id = chat_dict.get("id") or getrandbits(32)
            self.name = chat_dict.get("name") or "Chat"
            self.member_ids = chat_dict.get("member_ids") or member_ids
            message_list = chat_dict.get("messages") or []
            self.messages = [Message(message) for message in message_list] or messages
        else:
            self.id = id or getrandbits(32)
            self.name = name or "Chat"
            self.member_ids = member_ids
            self.messages = messages
        
        self._last_message = "Last message will be displayed here"
        self._member_picture_names = []

    def format_html(self, contacts):
        """Updates class variables for html generation. If called, exclusivly use object for html"""
        self._last_message = self.messages[-1].content if len(self.messages) > 0 else ""
        self._member_picture_names.clear()
        for contact in contacts:
            if contact.id in self.member_ids:
                self._member_picture_names.append(contact.picture_name)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "member_ids": self.member_ids,
            "messages": [message.to_dict() for message in self.messages],
        }