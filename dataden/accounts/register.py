import string

from flask import *
import json
import time

import mailservervice
import sqliteDB
from database import db, User, Verification
import tasklib

from serverconfig import Serverconfig

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

register = Blueprint("register", __name__, static_folder="static", template_folder="templates")


@register.route('/', methods=['GET', 'POST'])
def register_():
    if request.method == 'POST':
        time.sleep(1)
        print(request.form)
        if request.form['processtype'] == 'abortRegistration':  # abort register
            ### dont forget to write for sqlalchemy
            sqliteDB.sql(f'DELETE FROM verification WHERE mail=?', request.form["mail"])
            return jsonify({'visiturl': f'../register?registrationDel={request.form["mail"]}'})
        elif request.form['processtype'] == 'resendMail':  # send verification mail again
            ### dont forget to write for sqlalchemy
            if not sqliteDB.sql(f'SELECT EXISTS(SELECT 1 FROM verification WHERE mail=? LIMIT 1)', request.form["mail"]):
                return jsonify({'error': 'err02'})
            user_data = sqliteDB.to_json(sqliteDB.sql(f'SELECT * FROM verification WHERE mail=?', request.form["mail"]),
                                         table='verification')
            send_mail_status = mailservervice.sendmail(Serverconfig.get('server_mail'),
                                                       request.form["mail"],
                                                       'Data-Den Registration Verification',
                                                       mailservervice.generate_registermail(user_data['username'],
                                                                                            user_data['verification_id']))
            if not send_mail_status:
                return jsonify({'error': 'mailsenderror'})
            return jsonify({'visiturl': f'../register?userregistered={request.form["username"]}'})
        # mail
        if request.form['mail'] == '':
            return jsonify({'error': 'err00'})  # mail empty





        #elif sqliteDB.sql(f'SELECT EXISTS(SELECT 1 FROM userdata WHERE mail=? LIMIT 1)', request.form["mail"].lower(), 1):

        #    pass
        print("COcktime:")
        
        print(User.query.filter_by(mail='admin').first() is None)
        print("no cock ;(")
        if False:




            return jsonify({'error': 'err01'})  # mail already verified
        elif sqliteDB.sql(f'SELECT EXISTS(SELECT 1 FROM verification WHERE mail=? LIMIT 1)', request.form["mail"], 1):
            return jsonify(
                {'error': 'err03'})  # mail already within verification; (err02 is changeMail, so not needed on server)
        # password
        elif request.form['password'] == '':
            return jsonify({'error': 'err10'})  # password empty
        elif len(request.form['password']) < 8:
            return jsonify({'error': 'err11'})  # password too short
        elif len(request.form['password']) > 32:
            return jsonify({'error': 'err12'})  # password too long
        if not tasklib.stringcontents(request.form['password'],
                                      [string.digits, string.ascii_letters, string.punctuation]):
            return jsonify({'error': 'err13'})  # password illegal characters
        # confirmPassword
        elif len(request.form['password']) == '':
            return jsonify({'error': 'err20'})  # confirmPassword empty
        elif request.form['confirmPassword'] != request.form['password']:
            return jsonify({'error': 'err21'})  # confirmPassword not matching
        # username
        elif request.form['username'] == '':
            return jsonify({'error': 'err30'})  # username empty
        elif len(request.form['username']) < 3:
            return jsonify({'error': 'err31'})  # username too short
        elif len(request.form['username']) > 24:
            return jsonify({'error': 'err32'})  # username too long
        elif sqliteDB.sql(f'SELECT EXISTS(SELECT 1 FROM userdata WHERE username=? LIMIT 1)', request.form["username"], 1) or sqliteDB.sql(f'SELECT EXISTS(SELECT 1 FROM verification WHERE username=? LIMIT 1)', request.form["username"], 1):
            return jsonify({'error': 'err33'})  # username already exists
        elif not tasklib.stringcontents(request.form['username']):
            return jsonify({'error': 'err34'})  # username is not alpha-numerical
        verification_id = sqliteDB.new_user_id()
        send_mail_status = mailservervice.sendmail(Serverconfig.get('server_mail'),
                                                   request.form["mail"],
                                                   'Data-Den Registration Verification',
                                                   mailservervice.generate_registermail(request.form['username'],
                                                                                        verification_id))
        if not send_mail_status:
            return jsonify({'error': 'mailsenderror'})
        hash_salt = tasklib.generate_salt()

        db.session.add(Verification(id=verification_id, mail=request.form["mail"].lower(), username=request.form["username"], password=tasklib.hashData(request.form["password"], hash_salt), hash_salt=hash_salt))
        db.session.commit()

        return jsonify({'visiturl': f'../register?userregistered={request.form["username"]}'})

    elif 'userregistered' in request.args.keys():
        return render_template('showBigText.html',
                               show_text=f'<p>Hello {escape(request.args.get("userregistered"))}, we have sent a verification email to you. Once you have activated your account, click <a href="/login">here</a> to login.</p>',
                               **colorThemes['default'])
    elif 'registrationDel' in request.args.keys():
        return render_template('showBigText.html',
                               show_text=f'<p>{escape(request.args.get("registrationDel"))} is now deleted from our system and the registration process is stopped. You can alway register again, if you want to.</p>',
                               **colorThemes['default'])
    else:
        return render_template('register.html',
                               **colorThemes['default'])