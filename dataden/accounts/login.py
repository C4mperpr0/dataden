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
                               redirect_url=url_for('login.login_'),
                               **colorThemes['default'])
    else:
        time.sleep(1)
        check_login = sqliteDB.check_login(current_app,
                                           request.form['mail'],
                                           request.form['password'],
                                           current_app.DbClasses.User)
        if check_login is not None:
            session['user_id'] = check_login.id
            session['username'] = check_login.username
            session['user_mail'] = check_login.mail
            session['design'] = check_login.design
            return jsonify({'login': True})
        else:
            return jsonify({'error': 'loginerror'})
