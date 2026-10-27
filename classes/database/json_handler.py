import json
import os

CONTACTS_PATH = "static/database/contacts.json"
IDENTITY_PATH = "static/database/identity.json"
CHATS_PATH = "static/database/chats"

def load_file(path):
    with open(path, "r") as file:
        return json.load(file)

def save_file(path, data):
    with open(path, "w") as file:
        json.dump(data, file)