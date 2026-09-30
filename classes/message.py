class Message:
    def __init__(self, content=None, date=None, sender=None, read=None, msg_dict=None):
        if msg_dict:
            self.content = msg_dict["content"]
            self.date = msg_dict["date"]
            self.sender = msg_dict["sender"]
            self.read = msg_dict["read"]
        else:
            self.content = content or ""
            self.date = date or ""
            self.sender = sender or ""
            self.read = read or ""

    @property
    def dict_repr(self):
        return {
            "content": self.content,
            "date": self.date,
            "sender": self.sender,
            "read": self.read
        }