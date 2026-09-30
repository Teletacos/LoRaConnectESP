from classes.chat import Chat

class ChatsConverter():
    def __init__(self, fileHandler):
        self.fileHandler = fileHandler
  
    def dicts_to_chats(self, dicts):
        chats = []
        for chat_dict in dicts:
            chats.append(Chat(chat_dict=chat_dict))
        return chats

    def chats_to_dicts(self, chats):
        dicts = []
        for chat in chats:
            dicts.append(chat.dict_repr)
        return dicts
    
    def load_chats(self):
        return self.dicts_to_chats(self.fileHandler.load_data())

    def save_chats(self, chats):
        self.fileHandler.save_data(self.chats_to_dicts(chats))
