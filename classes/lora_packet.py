import ujson
import struct
from classes.database.message import Message

class LoraPacket:
    HEADER_FORMAT = ">IIB" # 255 characters content max, B=unsigned char 1 byte
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, message_id=0, chat_id=0, content="", encoded=None):
        if encoded:
            self.decode(encoded)
            return

        self.message_id = message_id
        self.chat_id = chat_id
        self.content = content
            
    def encode(self):
        content = self.content.encode("utf-8")
        header = struct.pack(
            self.HEADER_FORMAT,
            self.chat_id,
            self.message_id,
            len(content)
        )
        encoded = header + content
        print(f"Encoded packet size: {len(encoded)} bytes")
        return encoded

    def decode(self, encoded):
        if len(encoded) < self.HEADER_SIZE:
            raise ValueError("Invalid packet: header too short")
        
        print("Decoding", encoded)
        self.chat_id, self.message_id, content_length = struct.unpack(
            self.HEADER_FORMAT,
            encoded[:self.HEADER_SIZE]
        )
        content = encoded[self.HEADER_SIZE:]
        
        if len(content) != content_length:
            raise ValueError("Invalid packet: incorrect content length")

        self.content = content.decode("utf-8")