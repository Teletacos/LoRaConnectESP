from urandom import getrandbits

class Contact:
    def __init__(self, contact_dict=None, id=None, name=None, picture_name=None):
        if contact_dict:
            self.id = contact_dict.get("id") or getrandbits(32)
            self.name = contact_dict.get("name") or "Contact"
            self.picture_name = contact_dict.get("picture_name") or "default.png"
        else:
            self.id = id or getrandbits(32)
            self.name = name or "Contact"
            self.picture_name = picture_name or "default.png"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture_name": self.picture_name,
        }