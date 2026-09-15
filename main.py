from microdot import Microdot, Response, send_file, redirect
from multipart import with_form_data
from utemplate_micro import Template
import network
import json

user_data_path = "static/database/user.json"
chats_path = "static/database/chats.json"

def get_user_data():
    with open(user_data_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def write_chats(chats):
    with open(chats_path, "w") as file:
        json.dump(chats, file, indent=4)

def get_chats():
    with open(chats_path, "r", encoding="utf-8") as file:
        return json.load(file)

def get_last_msg(chat):
    if len(chat["messages"]) == 0: return "dawdaw"
    return chat["messages"][-1]["content"]

def get_last_date(chat):
    if len(chat["messages"]) == 0: return "Unknown"
    return chat["messages"][-1]["date"]

def get_notifications(chat):
    notification_amount = 0
    for message in chat["messages"]:
        if message["read"] == False:
            notification_amount += 1
    return notification_amount

def get_chats_preview(search_str=""):
    user_data = get_user_data()
    chats = get_chats()
    chats_preview = {}

    for chat_id, chat in chats.items():
        if chat_id == user_data["id"]: continue

        if search_str.lower() not in chat["name"].lower():
            continue

        chats_preview[chat_id] = {
            "name": chat["name"],
            "picture": chat["picture"],
            "last_msg": get_last_msg(chat),
            "last_date": get_last_date(chat),
            "notifications": get_notifications(chat)
        }

    return chats_preview

def setup_wifi():
    ssid = 'MicroPython-AP'
    password = '123456789'

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)

    while ap.active() == False:
        pass

    print('Connection successful')
    print(ap.ifconfig())

def setup_app():
    app = Microdot()
    Response.default_content_type = "text/html"

    @app.get("/")
    @app.post("/")
    @with_form_data
    def index(request):
        if request.method == 'POST':
            search_str = request.form.get("search")
        else:
            search_str = ""
        chats_preview = get_chats_preview(search_str)
        return Template("index.html").render(chats_preview)

    @app.post("/chat/new")
    @with_form_data
    def new_chat():
        chats = get_chats()

        chat_id = machine.rng()
        new_chat = {
            "name": "New Chat",
            "picture": "images/user-pics/profile.jpg",
            "messages": [
            ]
        }

        chats[chat_id] = new_chat
        write_chats(chats)

        return redirect("/")

    @app.post('/users')
    @app.get('/users/<int:chat_id>')
    @with_form_data
    def open_chat(request, chat_id):
        user_data = get_user_data()
        chats = get_chats()
        if not chat_id in chats: return redirect("/")
        chat = chats[chat_id]

        message_to_send = request.form.get("message", "")
        if len(message_to_send) > 0:
            new_message = {
                "content": message_to_send,
                "date": "Unkown",
                "sender": user_data["id"],
                "read": True
            }
            chat["messages"].append(new_message)
            write_chats(chats)

        print("Sent message", new_chat)
        return Template("chat.html").render(user_data=user_data, chat_id=chat_id, chat=chat)

    app.run(port=8000)

if __name__ == "__main__": 
    setup_wifi()
    setup_app()