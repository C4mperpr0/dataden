from flask import *
import json

from serverconfig import Serverconfig
import sqliteDB

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

verify = Blueprint("verify", __name__, static_folder="static", template_folder="templates")

@verify.route('/', methods=['GET', 'POST'])
def verify_():
    if request.method == 'GET':
        if 'u' not in request.args.keys():
            return redirect('/login')
        else:
            return render_template('verify.html',
                                   **colorThemes['default'])
    else:
        check_login = sqliteDB.check_login(current_app,
                                           request.form['mail'],
                                           request.form['password'],
                                           current_app.DbClasses.Verification,
                                           verification_key=request.args.get('u'))
        if check_login is not None:
            session['user_id'] = check_login.id
            session['username'] = check_login.username
            session['user_mail'] = check_login.mail
            session['design'] = 'default'
            return jsonify({'logged_in': True})
        else:
            return jsonify({'error': True})
