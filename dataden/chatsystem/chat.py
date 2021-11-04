from flask import *
from flask_socketio import Namespace, send, emit, join_room
import json
from difflib import get_close_matches
from datetime import datetime

from serverconfig import Serverconfig
import sqliteDB

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

chat = Blueprint("chat", __name__, static_folder="static", template_folder="templates")


@chat.route('/', methods=['GET', 'POST'])
def chat_():
    if 'user_id' in session.keys():
        if request.method == 'GET':
            return render_template('chat.html',
                                   **colorThemes['default'])
        else:
            return "post"

# Socket IO

class Socketio(Namespace):
    def on_connect(self):
        if 'user_id' in session.keys():
            join_room(session['user_id'])
            send({'joined': True}, to=session['user_id'])
        else:
            send({'join': False})

    def on_chatmessage(self, msg):
        if 'user_id' in session.keys():
            messages_id = sqliteDB.sql(f'SELECT message_id FROM messages WHERE chat_id = \"{msg["chat_id"]}\" ORDER BY message_id DESC LIMIT 1')[0][0] + 1
            sqliteDB.sql(f'INSERT INTO messages ("chat_id", "message_id", "message", "user_id", "time", "content") VALUES ({msg["chat_id"]}, {messages_id}, {msg["text"]}, {session["user_id"]}, {datetime.now()}, "{"{}"}")')
            
            # save msg in database
            # for user in chat send msg to them
            emit('chatmessage', msg, broadcast=True, to=session['user_id'])
        else:
            send({'join': False})

    def on_usernamesearch(self, data):
        usernames = sqliteDB.query(f'SELECT username FROM userdata')
        usernames.extend(sqliteDB.query(f'SELECT mail FROM userdata'))
        matches = get_close_matches(data['username'], list(u[0] for u in usernames), 10, .3)
        emit('usernamesearch', {'matches': matches, 'time': data['time'], 'exists': (data['username'] in usernames)},
             broadcast=True, to=session['user_id'])

    def on_chatcontrol(self, data):
        if data['process'] == 'getAllChats':
            all_chats = sqliteDB.to_json(sqliteDB.sql(f'SELECT * FROM chats WHERE members_id LIKE \'%{session["user_id"]}%\''),
                                        'chats',
                                         force_list=True)
            all_chats['messages'] = []
            for c in all_chats['chat_id']:
                all_chats['messages'].append(sqliteDB.sql(f'SELECT message_id FROM messages WHERE chat_id="{c}" ORDER BY message_id DESC LIMIT 1')[0][0])
            emit('chatcontrol', {'process': 'getAllChats', 'username': session['username'], 'data': all_chats}, broadcast=True, to=session['user_id'])
            print({'process': 'getAllChats', 'username': session['username'], 'data': all_chats})
        elif data['process'] == 'newDm':
            # check before if dm chat already exists
            usernames = sqliteDB.sql(f'SELECT username FROM userdata')
            mails = sqliteDB.sql(f'SELECT mail FROM userdata')
            if (data['username'],) in usernames:  # matching with 1 Element tuple bc Select returns Items as tuple
                new_chat_partner = sqliteDB.to_json(sqliteDB.sql(f'SELECT * FROM userdata WHERE username="{data["username"]}"'),
                                                    'userdata')
            elif (data['username'],) in mails:
                new_chat_partner = sqliteDB.to_json(sqliteDB.sql(f'SELECT * FROM userdata WHERE mail="{data["username"]}"'),
                                                    'userdata')
            new_chat_id = sqliteDB.new_chat_id()
            sqliteDB.sql(f'INSERT INTO chats ("chat_id", "members_id", "members_name", "type") VALUES ({new_chat_id}, {",".join([new_chat_partner["user_id"], session["user_id"]])}, {",".join([new_chat_partner["username"], session["username"]])}, "dm")')
            sqliteDB.sql(f'INSERT INTO messages ("chat_id", "message_id", "user_id", "time", "content") VALUES ({new_chat_id}, {0}, "SERVER", {datetime.now()}, "{{"msg_type": "chatinfo"}}")')
            emit('chatcontrol', {'process': 'refresh'}, broadcast=True, to=session['user_id'])
