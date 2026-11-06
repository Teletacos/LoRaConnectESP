class Message:
    STATUS_LABELS = ["Pending", "Sent", "Received", "Failed"]
    PENDING = 0
    SENT = 1
    RECEIVED = 2
    FAILED = 3

    def __init__(self, message_dict=None, id=0, sender_id=0, content="", status=0):
        if message_dict:
            self.id = message_dict.get("id") or id
            self.sender_id = message_dict.get("sender_id") or sender_id
            self.content = message_dict.get("content") or content
            self.status = message_dict.get("status") or status
        else:
            self.id = id
            self.sender_id = sender_id
            self.content = content
            self.status = status

        self._picture_name = ""
        self._is_sender = False

    def format_html(self, identity, contacts):
        self.status = self.STATUS_LABELS[self.status], 
        
        if self.sender_id == identity.id:
            self._picture_name = identity.picture_name
            self._is_sender = True
        else:
            contact = None
            for c in contacts:
                if c.id == self.sender_id:
                    contact = c
                    break
        
        if contact:
            self._picture_name = contact.picture_name
            self._is_sender = False


    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content,
            "status": self.status,
        }