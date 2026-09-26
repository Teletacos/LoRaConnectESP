import uuid

class Chat:
    def __init__(self, id=None, name=None, picture_name=None, messages=None):
        self.id = id or str(uuid.uuid4())
        self.name = name or "User"
        self.picture_name = picture_name or "profile.jpg"
        self.messages = messages or []

    @property
    def picture_path(self):
        return f"images/user-pics/{self.picture_name}"

    @property
    def last_msg(self):
        if len(self.messages) == 0: return ""
        return self.messages[-1]["content"]

    @property
    def last_date(self):
        if len(self.messages) == 0: return ""
        return self.messages[-1]["date"]

    @property
    def notifications(self):
        amount = 0
        for message in self.messages:
            if message["read"] == False:
                amount += 1
        return amount