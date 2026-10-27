class Identity:
    def __init__(self, identity_dict):
        self.id = identity_dict.get("id") or ""
        self.name = identity_dict.get("name") or ""
        self.picture_name = identity_dict.get("picture_name") or ""

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture_name": self.picture_name,
        }