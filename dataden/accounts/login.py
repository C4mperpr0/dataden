from flask import *
import json
import time

from serverconfig import Serverconfig
import sqliteDB

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

login = Blueprint("login", __name__, static_folder="static", template_folder="templates")

@login.route('/', methods=['GET', 'POST'])
def login_():
    if request.method == 'GET':
        if 'user_id' in session.keys():
            return f"moin {escape(session['username'])}"
        return render_template('login.html',
                               **colorThemes['default'])
    else:
        time.sleep(1)
        check_login = sqliteDB.check_login(request.form['mail'], request.form['password'], 'userdata')
        if check_login is not None:
            session['user_id'] = check_login['user_id']
            session['username'] = check_login['username']
            session['user_mail'] = check_login['mail']
            session['design'] = 'default'
            """
            return render_template('login.html',
                                   redirect_to=(
                                       request.args.get("redirect") if 'redirect' in request.args else '/'),
                                   **colorThemes['default'])
            """
            return jsonify({'visiturl': '/'})
        else:
            return jsonify({'error': 'loginerror'})