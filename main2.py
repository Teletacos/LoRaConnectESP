from lib.microdot import Microdot, Response, send_file, redirect
from lib.multipart import with_form_data
from lib.jinja import Template
from classes.chatsConverter import ChatsConverter
from classes.chatsFormatter import ChatsFormatter
from classes.jsonHandler import JSONHandler

def setup_app():
    app = Microdot()
    Response.default_content_type = "text/html"

    deviceJSONHandler = JSONHandler("static/database/device.json")
    chatsJSONHandler = JSONHandler("static/database/chats.json")
    chatsConverter = ChatsConverter(chatsJSONHandler)
    chatsFormatter = ChatsFormatter()

    @app.route('/static/<path:path>')
    def static(request, path):
        print(path)
        if '..' in path:  # Prevent directory traversal attacks
            return 'Not found', 404
        return send_file('static/' + path)

    @app.get("/index")   
    @app.post("/index")
    @app.get("/")
    @app.post("/")
    @with_form_data
    def index(request):
        search_str = ""
        if request.method == 'POST':
            search_str = request.form.get("search", "")
        chats = chatsConverter.load_chats()
        chats_previews = chatsFormatter.get_chats_previews(chats)
        return Template("index.html").render(chats_previews=chats_previews, current_search=search_str)

    @app.get("/chat/<chat_id>")
    @app.post("/chat/<chat_id>")
    def open_chat(request, chat_id):
        user_data = deviceJSONHandler.load_data()
        chats = chatsConverter.load_chats()
        chat = chatsFormatter.get_chat_from_id(chats, chat_id)
        if not chat: return redirect("/index")

        if request.method == "POST":
            message_to_send = request.form.get("message", "")
            if len(message_to_send) > 0:
                new_message = {
                    "content": message_to_send,
                    "date": "Unkown",
                    "sender": user_data["id"],
                    "read": True
                }
                chat.messages.append(new_message)
                chatsConverter.save_chats(chats)

        return Template("chat.html").render(user_data=user_data, chat_id=chat_id, chat=chat)

    return app

app = setup_app()
app.run(port=80)