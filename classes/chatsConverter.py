from classes.chat import Chat

class ChatsConverter():
    chat_properties = ["id", "name", "picture_name", "messages"]

    def __init__(self, fileHandler):
        self.fileHandler = fileHandler

    def dict_to_chat(self, dictionary):
        arguments = [dictionary[property] for property in ChatsConverter.chat_properties]
        chat = Chat(*arguments)
        return chat

    def chat_to_dict(self, chat):
        dictionary = {}
        for property in ChatsConverter.chat_properties:
            dictionary[property] = getattr(chat, property)
        return dictionary
            
    def dicts_list_to_chats_list(self, dicts_list):
        chats_list = []
        for dictionary in dicts_list:
            chats_list.append(self.dict_to_chat(dictionary))
        return chats_list

    def chats_list_to_dicts_list(self, chats_list):
        dicts_list = []
        for chat in chats_list:
            dicts_list.append(self.chat_to_dict(chat))
        return dicts_list
    
    def load_chats(self):
        return self.dicts_list_to_chats_list(self.fileHandler.load_data())

    def save_chats(self, chats):
        self.fileHandler.save_data(self.chats_list_to_dicts_list(chats))
