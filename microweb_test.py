import gc
import classes.database.data_handler as data_handler
import classes.database.data_formatter as data_formatter
from classes.lora_sender import LoraSender
from classes.database.message import Message

import lib.microweb.wifi as wifi
from lib.microweb.microweb import MicroWeb, Response, FileResponse

identity = data_handler.get_identity()
lora_sender = LoraSender(identity.id)

app = MicroWeb(debug=True, ap={"ssid": identity.name, "password": identity.password})

app.add_static("/static/manifest.json", "static/manifest.json")
app.add_static("/static/css/general.css", "static/css/general.css")
app.add_static("/static/css/index.css", "static/css/index.css")
app.add_static("/static/css/chat.css", "static/css/chat.css")
app.add_static("/static/images/icons/add.svg", "static/images/icons/add.svg")
app.add_static("/static/images/icons/search.svg", "static/images/icons/search.svg")
app.add_static("/static/images/icons/arrow-back.svg", "static/images/icons/arrow-back.svg")
app.add_static("/static/images/icons/arrow-up.svg", "static/images/icons/arrow-up.svg")
app.add_static("/static/images/user-pics/kristina.png", "static/images/user-pics/kristina.png")
app.add_static("/static/images/user-pics/walter.png", "static/images/user-pics/walter.png")

def url_decode(value):
    result = bytearray()
    i = 0

    while i < len(value):
        if value[i] == '+':
            result.append(32)
            i += 1
        elif value[i] == '%' and i + 2 < len(value):
            try:
                result.append(int(value[i + 1:i + 3], 16))
                i += 3
            except ValueError:
                result.extend(value[i].encode())
                i += 1
        else:
            result.extend(value[i].encode("utf-8"))
            i += 1

    return result.decode("utf-8")

@app.route('/')
def home(request):
    gc.collect()

    search_str = ""
    if request.method == "POST":
        search_str = request.form.get("search")

    chats = data_handler.get_all_chats()
    selected_chats = data_formatter.contains(chats, name=search_str)
    return app.render_template('static/index.html', identity=identity, chats=selected_chats)   

@app.route("/chat/<chat_id>", methods=["GET", "POST"])
def open_chat(request, match):
    gc.collect()
    
    chat_id = match.group(1)
    contacts = data_handler.get_all_contacts()
    chat = data_handler.get_chat(chat_id)

    chat.messages = chat.messages[-20:] # Last 20 messages
    for message in chat.messages:
        message.format_html(identity, contacts)

    if request.method == "POST":
        form_message = request.form.get("message", "") 
        message_to_send = url_decode(form_message)
        if 0 < len(message_to_send) < 100:
            message = Message(id=len(chat.messages), sender_id=identity.id, content=message_to_send, status=Message.PENDING)
            recv_id = [x for x in chat.member_ids if x != identity.id][0]
            ack = lora_sender.send_message(message, chat_id, recv_id)
            return app.redirect(f"/chat/{chat_id}")
    return app.render_template('static/chat.html', identity=identity, chat=chat)    

@app.route('/api/data', methods=['GET'])
def data(req):
    return app.json_response(data_handler.get)

app.run()