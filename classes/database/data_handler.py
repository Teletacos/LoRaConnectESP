import os
import classes.database.json_handler as file_handler

from classes.database.identity import Identity
from classes.database.contact import Contact
from classes.database.chat import Chat


# Identity
def get_identity():
    return Identity(file_handler.load_file(file_handler.IDENTITY_PATH))


def save_identity(identity):
    file_handler.save_file(file_handler.IDENTITY_PATH,identity.to_dict())


# Contacts
def get_all_contacts():
    data = file_handler.load_file(file_handler.CONTACTS_PATH)
    return [Contact(contact) for contact in data]


def get_contact(id):
    for contact in get_all_contacts():
        if contact.id == id:
            return contact
    return None

def add_contact(contact):
    contacts = get_all_contacts()
    for c in contacts:
        if c.id == contact.id:
            return
    contacts.append(contact)
    file_handler.save_file(
        file_handler.CONTACTS_PATH,
        [item.to_dict() for item in contacts]
    )

def edit_contact(id, contact):
    contacts = get_all_contacts()
    for c in contacts:
        if c.id == id:
            c.id = contact.id
            c.name = contact.name
            break
    file_handler.save_file(
        file_handler.CONTACTS_PATH,
        [item.to_dict() for item in contacts]
    )

# Chats
def get_all_chats():
    chats = []
    for filename in os.listdir(file_handler.CHATS_PATH):
        if filename.endswith(".json"):
            path = file_handler.CHATS_PATH + "/" + filename
            chats.append(
                Chat(file_handler.load_file(path))
            )
    return chats


def get_chat(id):
    path = file_handler.CHATS_PATH + "/" + str(id) + ".json"
    try:
        return Chat(file_handler.load_file(path))
    except FileNotFoundError:
        return None

def save_chat(chat):
    path = file_handler.CHATS_PATH + "/" + str(chat.id) + ".json"
    file_handler.save_file(path, chat.to_dict())

def edit_chat(id, chat):
    existing = get_chat(id)
    if not existing: return
    id_changed = id != chat.id
    old_path = file_handler.CHATS_PATH + "/" + str(existing.id) + ".json"

    existing.id = chat.id
    existing.name = chat.name
    existing.member_ids = chat.member_ids
    save_chat(existing)

    if id_changed:
        file_handler.delete_file(old_path)
        
# Message
def add_message(message, chat_id):
    chat = get_chat(chat_id)
    chat.messages.append(message)
    save_chat(chat)

def set_message(message, chat_id):
    chat = get_chat(chat_id)
    found_chat = False
    for i in range(len(chat.messages)):
        if chat.messages[i].id == message.id:
            chat.messages[i] = message
            found_chat = True
            break
    if not found_chat:
        chat.messages.append(message)
    save_chat(chat)