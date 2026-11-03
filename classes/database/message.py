class Message:
    def __init__(self, message_dict):
        self.id = message_dict.get("id") or "msg_000"
        self.sender_id = message_dict.get("sender_id") or 0
        self.content = message_dict.get("content") or ""
        self.created_at = message_dict.get("created_at") or "2026-10-20"
        self.status = message_dict.get("status") or "unknown"
        self.picture_name = ""
        self.is_sender = False

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content,
            "created_at": self.created_at,
            "status": self.status,
        }