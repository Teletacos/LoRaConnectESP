class ChatsFormatter:
    def __init__(self):
        pass

    def sort_by(self, chats, key_name="", reverse=False):
        return sorted(chats, key=lambda item: item[key_name], reverse=reverse)

    def exclude(self, chats, id="", name=""):
        selected = []
        for chat in chats:
            if id and (id == chat.id):
                continue
            if name and (name in chat.name):
                continue
            selected.append(chat)
        return selected

    def select(self, chats, id=None, name=None, search=None):
        selected = []
        for chat in chats:
            if id and (id != chat.id):
                continue
            if name and (name != chat.name):
                continue
            if search and (search.lower() not in chat.name.lower()):
                continue
            selected.append(chat)
        return selected