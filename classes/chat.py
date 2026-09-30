from lib.uuid import uuid4
from classes.message import Message

class Chat:
    def __init__(self, id=None, name=None, picture_name=None, messages=None, chat_dict=None):
        if chat_dict:
            self.id = chat_dict["id"]
            self.name = chat_dict["name"]
            self.picture_name = chat_dict["picture_name"]
            self.messages = [Message(msg_dict=msg_dict) for msg_dict in chat_dict["messages"]]
        else:
            self.id = id or str(uuid4())
            self.name = name or "User"
            self.picture_name = picture_name or "kristina.png"
            self.messages = messages or []
    
    @property
    def picture_path(self):
        return f"images/user-pics/{self.picture_name}"

    @property
    def last_msg(self):
        if len(self.messages) == 0: return ""
        return self.messages[-1].content

    @property
    def last_date(self):
        if len(self.messages) == 0: return ""
        return self.messages[-1].date

    @property
    def notifications(self):
        amount = 0
        for message in self.messages:
            if message.read == False:
                amount += 1
        return amount

    @property
    def dict_repr(self):
        messages = [message.dict_repr for message in self.messages]
        return {
            "id": self.id,
            "name": self.name,
            "picture_name": self.picture_name,
            "messages": messages
        }

    def __str__(self):
        return self.id