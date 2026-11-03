import ujson
import os

CONTACTS_PATH = "static/database/contacts.json"
IDENTITY_PATH = "static/database/identity.json"
CHATS_PATH = "static/database/chats"

def load_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return ujson.load(file)

def save_file(path, data):
    with open(path, "w", encoding="utf-8") as file:
        ujson.dump(data, file)