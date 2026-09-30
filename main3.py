import network
from lib.microdot.microdot import Microdot, send_file, Response
from lib.microdot.utemplate_micro import Template
from classes.chatsConverter import ChatsConverter
from classes.chatsFormatter import ChatsFormatter
from classes.jsonHandler import JSONHandler
from classes.message import Message
from classes.chat import Chat
import asyncio

app = Microdot()
Response.default_content_type = "text/html"

def setup_wifi():
    ssid = 'MicroPython-AP'
    password = '123456789'

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)

    print('Wi-Fi Connection successful')
    print(ap.ifconfig())

@app.route('/')
async def index(request):
    return Template("index.html").render()

@app.route("/impede")
async def impede(request):
    while True:
        print("AA")
        await asyncio.sleep(0.1)

@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:  # Prevent directory traversal attacks
        return 'Not found', 404
    return send_file('static/' + path)

async def counter():
    i = 0
    while True:
        i += 1
        print(i)
        await asyncio.sleep(1)

setup_wifi()
async def main():
    asyncio.create_task(counter())
    await app.run(debug=True, port=5000, host="0.0.0.0")

asyncio.run(main())