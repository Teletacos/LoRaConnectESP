import ujson
from classes.database.message import Message

class LoraPacket:
    def __init__(self, message=None, chat_id="", encoded=None):
        self.message = message
        self.chat_id = chat_id
        if encoded:
            print("Decoding")
            self.decode(encoded)
            
    def encode(self):
        return ujson.dumps(self.to_dict()).encode("utf-8")

    def decode(self, encoded):
        print("Decoding", encoded)
        encoded = encoded.decode("utf-8")
        print("Unloaded JSON: ", encoded)
        msg_dict = ujson.loads(encoded)
        print("Loaded JSON: ", msg_dict)
        self.message = Message(msg_dict["message"])
        self.chat_id = msg_dict["chat_id"]

    def to_dict(self):
        return {
            "message": self.message.to_dict(),
            "chat_id": self.chat_id
        }