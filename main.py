import gc
import time
import _thread
import asyncio
import classes.database.data_handler as data_handler
import classes.database.data_formatter as data_formatter
from classes.lora_sender import LoraSender
from classes.database.message import Message
from classes.database.contact import Contact


import lib.microweb.wifi as wifi
from lib.microweb.microweb import MicroWeb, Response, FileResponse

MESSAGE_COOLDOWN = 1000
last_message_time = 0

identity = data_handler.get_identity()
lora_sender = LoraSender(identity.id)

app = MicroWeb(debug=True, ap={"ssid": identity.name, "password": identity.password})

app.add_static("/static/manifest.json", "static/manifest.json")
app.add_static("/static/css/general.css", "static/css/general.css")
app.add_static("/static/css/index.css", "static/css/index.css")
app.add_static("/static/css/chat.css", "static/css/chat.css")
app.add_static("/static/css/contacts.css", "static/css/contacts.css")
app.add_static("/static/images/icons/add.svg", "static/images/icons/add.svg")
app.add_static("/static/images/icons/search.svg", "static/images/icons/search.svg")
app.add_static("/static/images/icons/arrow-back.svg", "static/images/icons/arrow-back.svg")
app.add_static("/static/images/icons/arrow-up.svg", "static/images/icons/arrow-up.svg")
app.add_static("/static/images/icons/group.svg", "static/images/icons/group.svg")
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

@app.route('/', methods=["GET", "POST"])
@app.route('/chats', methods=["GET", "POST"])
def chats(request):
    gc.collect()

    search_str = ""
    if request.method == "POST":
        search_str = url_decode(request.form.get("search"))

    print("Here 1")
    contacts = data_handler.get_all_contacts()
    chats = data_handler.get_all_chats()
    selected_chats = data_formatter.contains(chats, name=search_str)
    print("Here 2")
    for chat in selected_chats:
        chat.format_html(contacts)
    print("Here 3")
    return app.render_template('static/index.html', identity=identity, chats=selected_chats, current_search=search_str)   

@app.route("/chats/add", methods=["POST"])
def add_chat(request):
    contacts = data_handler.get_all_contacts()
    member_ids = []
    for contact in contacts:
        print(request.form)
        #form_value = url_decode(request.form.getlist("checkbox"))
    try:
        contact_id =  url_decode(request.form.get("id"))
    except ValueError:
        return
    contact_name =  url_decode(request.form.get("name"))
    data_handler.add_contact(contact_id, Contact(id=contact_id, name=contact_name))

@app.route('/contacts', methods=["GET", "POST"])
def contacts(request):
    gc.collect()

    contacts = data_handler.get_all_contacts()
    return app.render_template('static/contacts.html', identity=identity, contacts=contacts)   

@app.route("/contacts/add", methods=["POST"])
def add_contact(request):
    try:
        contact_id =  url_decode(request.form.get("id"))
    except ValueError:
        return
    contact_name =  url_decode(request.form.get("name"))
    data_handler.add_contact(contact_id, Contact(id=contact_id, name=contact_name))

@app.route("/contact/edit/<contact_id>", methods=["POST"])
def edit_contact(request, match):
    try:
        contact_id = int(match.group(1))
        new_id =  int(url_decode(request.form.get("id")))
    except ValueError:
        print("Failed to convert edit contact info to int")
        return
    new_name =  url_decode(request.form.get("name"))
    data_handler.edit_contact(contact_id, Contact(id=new_id, name=new_name))

@app.route("/chat/<chat_id>", methods=["GET", "POST"])
def open_chat(request, match):
    gc.collect()

    chat_id = int(match.group(1))
    chat = data_handler.get_chat(chat_id)
    message_amount = len(chat.messages)

    if request.method == "POST":
        global last_message_time
        if time.ticks_diff(time.ticks_ms(), last_message_time) < MESSAGE_COOLDOWN:
            return app.redirect(f"/chat/{chat_id}")

        form_message = request.form.get("message", "") 
        message_to_send = url_decode(form_message)
        if 0 < len(message_to_send) < 100:
            message = Message(id=message_amount, sender_id=identity.id, content=message_to_send, status=Message.PENDING)
            recv_id = [x for x in chat.member_ids if x != identity.id][0]
            ack = lora_sender.send_message(message, chat_id, recv_id)
            if ack:
                last_message_time = time.ticks_ms()
            return app.redirect(f"/chat/{chat_id}")
    return app.render_template('static/chat.html', identity=identity, chat=chat)    

@app.route("/chat/<chat_id>/messages")
def get_messages(request, match):
    chat = data_handler.get_chat(int(match.group(1)))
    contacts = data_handler.get_all_contacts()
    chat.messages = chat.messages[-20:]

    for message in chat.messages:
        message.format_html(identity, contacts)

    return app.render_template(
        "static/messages.html",
        chat=chat
    )

async def main():
    _thread.start_new_thread(app.run, ())
    await lora_sender.send_queue()

asyncio.run(main())