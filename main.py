from lib.microdot.microdot import Microdot, Response, send_file, redirect
from lib.microdot.multipart import with_form_data
from lib.microdot.utemplate_micro import Template

import classes.database.data_handler as data_handler
import classes.database.data_formatter as data_formatter
from classes.sender import Sender
from classes.database.message import Message

import classes.wifi as wifi

app = Microdot()
Response.default_content_type = "text/html"

@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:  # Prevent directory traversal attacks
        return 'Not found', 404
    print(path)
    return send_file('static/' + path)

@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
async def index(request):
    search_str = ""
    if request.method == "POST":
        search_str = request.form.get("search")

    identity = data_handler.get_identity()
    chats = data_handler.get_all_chats()
    selected_chats = data_formatter.contains(chats, name=search_str)
    return Template("index.html").render(identity=identity, chats=selected_chats)

@app.route("/chat/<chat_id>", methods=["GET", "POST"])
async def open_chat(request, chat_id):
    print("Opening chat:", chat_id)
    identity = data_handler.get_identity()
    chat = data_handler.get_chat(chat_id)

    return "ADW"

    try:
        identity = data_handler.get_identity()

        if request.method == "POST":
            print("POST")
            message_to_send = request.form.get("message", "")
            if 0 < len(message_to_send) < 100:
                message = Message({
                    "id": "13",
                    "sender_id": identity.id,
                    "content": message_to_send,
                    "created_at": "2020-01-01",
                    "status": "pending",
                })
                #lora_sender.send_message(message, chat_id)
        else:
            print("GET")

        chat = data_handler.get_chat(chat_id)
        print("CHAT DATA: ", chat.messages)

        html = Template("chat.html").render(
            identity=identity,
            chat=chat
        )
        print("Rendered HTML length:", len(html))
        return redirect("/index")

    except Exception as e:
        print("Chat route error:", repr(e))
        return "Internal server error", 500
    
#lora_sender = Sender()
wifi.run()
#app.run(debug=True, port=80, host="0.0.0.0")

#asyncio.run(main())