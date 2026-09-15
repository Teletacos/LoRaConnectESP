from machine import Pin
import network
from microdot import Microdot, Response, send_file, redirect
from utemplate_micro import Template

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
    led_pin = Pin(26, Pin.OUT) 

    @app.route("/")
    async def index(request):
        led_status = "On" if led_pin.value() == 1 else "Off"
        return Template("index.html").render(led_status=led_status)

    @app.route("/on")
    async def toggle(request):
        led_pin.on()
        return redirect('/')

    @app.route("/off")
    async def wassup(request):
        led_pin.off()
        return redirect('/')

    @app.route('/static/<path:path>')
    async def static(request, path):
        if '..' in path:
            # directory traversal is not allowed
            return 'Not found', 404
        return send_file('static/' + path)

    app.run(port=80)

setup_wifi()
setup_app()

