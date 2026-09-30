import network
from lib.microdot.microdot import Microdot, Response, send_file, redirect
from lib.microdot.multipart import with_form_data
from lib.microdot.utemplate_micro import Template
from classes.chatsConverter import ChatsConverter
from classes.chatsFormatter import ChatsFormatter
from classes.jsonHandler import JSONHandler
from classes.message import Message
from classes.chat import Chat
import asyncio

# Config
WIFI_SSID = 'MicroPython-AP'
WIFI_PASS = '123456789'
DEVICE_ID = "0caad66b-f669-4c19-9549-7df2d4f89a8e"
DB_PATH = "static/database/chats.json"
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

# Setup
app = Microdot()
Response.default_content_type = "text/html"

chats_json_handler = JSONHandler(DB_PATH)
chats_converter = ChatsConverter(chats_json_handler)
chats_formatter = ChatsFormatter()

def setup_wifi():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=WIFI_SSID, password=WIFI_PASS)

    while not ap.active():
        pass

    print('Wi-Fi Connection successful')
    print(ap.ifconfig())

@app.route('/static/<path:path>')
async def static(request, path):
    print(path)
    if '..' in path:  # Prevent directory traversal attacks
        return 'Not found', 404
    return send_file('static/' + path, max_age=3600)

@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
@with_form_data
async def index(request):
    search_str = ""
    if request.method == 'POST':
        search_str = request.form.get("search", "")
    chats = chats_converter.load_chats()
    chats = chats_formatter.exclude(chats, id=DEVICE_ID)
    chats = chats_formatter.select(chats, search=search_str)
    print(search_str, chats)
    return Template("index.html").render(chats=chats, current_search=search_str)

@app.route("/chat/<chat_id>", methods=["GET", "POST"])
async def open_chat(request, chat_id):
    chats = chats_converter.load_chats()
    device_chats = chats_formatter.select(chats, id=DEVICE_ID)
    chats = chats_formatter.select(chats, id=chat_id)
    if not device_chats or not chats:
        return redirect("/index")
    device_chat = device_chats[0]
    chat = chats[0]

    if request.method == "POST":
        message_to_send = request.form.get("message", "")
        if len(message_to_send) > 0:
            new_message = Message(content=message_to_send, sender=DEVICE_ID)
            chat.messages.append(new_message)
            chats_converter.save_chats(chats)
    return Template("chat.html").render(device_chat=device_chat, chat=chat)

@app.post("/new_chat")
async def create_chat(request):
    chats = chats_converter.load_chats()
    new_chat = Chat()
    chats.append(new_chat)
    for chat in chats:
        print(chat.id)
    chats_converter.save_chats(chats)
    return redirect("/index")

setup_wifi()
async def main():
    await app.run(debug=True, port=5000, host="0.0.0.0")

asyncio.run(main())