from flask import *
from flask_socketio import Namespace, emit
import json

from serverconfig import Serverconfig

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

bettersentense = Blueprint("bettersentense", __name__, static_folder="static", template_folder="templates", static_url_path='/static/bettersentense')


@bettersentense.route('/', methods=['GET', 'POST'])
def bettersentense_():
    #print("hey")
    #if 'user_id' in session.keys():
    if request.method == 'GET':
        return render_template('bettersentense.html',
                               **colorThemes['default'])
    else:
        return "post"


# socket_io

class Socketio(Namespace):
    def on_merp(self, position):
        emit('merp', position, broadcast=True)