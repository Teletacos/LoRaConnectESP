class ChatsFormatter:
    def __init__(self):
        pass

    def search_filter(self, chats, search):
        filtered = []
        for chat in chats:
            if search in chats.name:
                filtered.append(chat)
        return filtered

    def get_chat_from_id(self, chats, id):
        for chat in chats:
            if chat.id == id:
                return chat
        return None

    def get_chats_previews(self, chats):
        previews = []
        for chat in chats:
            previews.append({
                "id": chat.id,
                "name": chat.name,
                "last_msg": chat.last_msg,
                "picture_path": chat.picture_path,
                "notifications": chat.notifications,
            })
        return previews