from flask import *
from flask_socketio import Namespace, emit, join_room
import json
from time import time
from serverconfig import Serverconfig

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

remoteControl = Blueprint("remoteControl", __name__, static_folder="static", template_folder="templates",
                          static_url_path='/static/remoteControl')


@remoteControl.route('/', methods=['GET', 'POST'])
def remoteControl_():
    # if 'user_id' not in session.keys():
    #     return render_template('login.html',
    #                            redirect_url=request.url,
    #                            **colorThemes['default'])
    if request.method == 'GET':
        return render_template('remoteControl.html',
                               redirect_url=request.url,
                               **colorThemes['default'])
    else:
        return "post"


# socket_io
with open('./remoteControl/runfile.py', 'r') as file:
    runfile = file.read()


class Socketio(Namespace):
    devices = {}

    def on_connect_room(self, device_id):
        if self.devices.has_key(device_id):
            if self.devices[device_id] > (round(time()) - 60):
                emit('go_down')
        else:
            self.devices[device_id] = round(time())
            join_room(device_id)

    def on_ping(self):
        print(request.args)

    def on_command(self, command, device_id):
        print(command)
        emit('command', command, room=device_id)

    def on_send_runfile(self):
        emit('runfile', runfile)
