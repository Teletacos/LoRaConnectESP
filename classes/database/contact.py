class Contact:
    def __init__(self, contact_dict, id=0, name="User", picture_name="default.png"):
        if contact_dict:
            self.id = contact_dict.get("id") or id
            self.name = contact_dict.get("name") or name
            self.picture_name = contact_dict.get("picture_name") or picture_name
        else:
            self.id = id
            self.name = name
            self.picture_name = picture_name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "picture_name": self.picture_name,
        }