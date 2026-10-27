class Contact:
    def __init__(self, contact_dict):
        self.id = contact_dict.get("id") or ""
        self.name = contact_dict.get("name") or ""
        self.picture_name = contact_dict.get("picture_name") or ""
        self.last_seen = contact_dict.get("last_seen") or 0

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture_name": self.picture_name,
            "last_seen": self.last_seen,
        }