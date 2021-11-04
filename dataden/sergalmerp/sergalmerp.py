from flask import *
from flask_socketio import Namespace, emit
import json

from serverconfig import Serverconfig

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

sergalmerp = Blueprint("sergalmerp", __name__, static_folder="static", template_folder="templates", static_url_path='/static/sergalmerp')


@sergalmerp.route('/', methods=['GET', 'POST'])
def sergalmerp_():
    #print("hey")
    #if 'user_id' in session.keys():
    if request.method == 'GET':
        return render_template('sergalmerp.html',
                               **colorThemes['default'])
    else:
        return "post"


# socket_io

class Socketio(Namespace):
    def on_merp(self, position):
        emit('merp', position, broadcast=True)