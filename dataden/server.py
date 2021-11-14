from flask import *
from flask_socketio import SocketIO
import json
import os

from serverconfig import Serverconfig
import sqliteDB
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

import accounts
import fileupload
import chatsystem
import sergalmerp
import remoteControl

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

app = Flask(__name__)
app.config['SECRET_KEY'] = Serverconfig.config['session_secret_key']
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False,
                    cors_allowed_origins='*')  # cors_allowed_origins='*' is for session access

from database import db
db.create_all()

app.register_blueprint(accounts.login.login, url_prefix="/login")
app.register_blueprint(accounts.register.register, url_prefix="/register")
app.register_blueprint(accounts.verify.verify, url_prefix="/verify")
app.register_blueprint(fileupload.fileupload.fileupload, url_prefix="/fileupload")
app.register_blueprint(chatsystem.chat.chat, url_prefix="/chat")
socketio.on_namespace(chatsystem.chat.Socketio('/chat'))
app.register_blueprint(sergalmerp.sergalmerp.sergalmerp, url_prefix="/sergalmerp")
socketio.on_namespace(sergalmerp.sergalmerp.Socketio('/sergalmerp'))
app.register_blueprint(remoteControl.remoteControl.remoteControl, url_prefix="/rc")
socketio.on_namespace(remoteControl.remoteControl.Socketio('/rc'))


@app.route('/loginred')
def loginred():
    return '<html><body> <form action="../login", method="GET"> <input tpye="text", name="redirect"/> <input type="submit" value="submit" /> </form> </body></html>'


@app.route('/delme')
def hi():
    if 'user_id' in session.keys():
        sqliteDB.sql(f'DELETE FROM userdata WHERE user_id="{session["user_id"]}"')
        mail = session['user_mail']
        session.clear()
        return f"Your Account \"{escape(mail)} is now deleted from our system!"
    else:
        return "You cannot delete your account when you are not logged in!"


@app.route('/')
def index():
    if 'user_mail' in session:
        return "Hallo " + escape(session['user_mail']) + '! Visit /delme to delete your account!'
    else:
        return "<h1>Meld dich doch an du wichser!</h1><a href='login'>Login</a>"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    socketio.run(app,
                 port=Serverconfig.config['server_port'],
                 host=Serverconfig.config['server_ip'],
                 debug=Serverconfig.config['debug'])  # threaded=Serverconfig.config['threading'])
