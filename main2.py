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

#lora_sender = Sender()

wifi.run()
#app.run(debug=True, port=80, host="0.0.0.0")

#asyncio.run(main())