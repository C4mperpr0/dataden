from flask import *
from werkzeug.utils import secure_filename
import json
import os

from serverconfig import Serverconfig

Serverconfig = Serverconfig()

# import color themes
with open('./templateColors.json', 'r') as file:
    global colorThemes
    colorThemes = json.loads(file.read())

fileupload = Blueprint("fileupload", __name__, static_folder="static", template_folder="templates")

#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    """
    print('.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    """
    return True
@fileupload.route('/', methods=['GET', 'POST'])
def fileupload_():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Serverconfig.get('fileuploadpath'), filename))
            return redirect(url_for("fileupload.fileupload_"))
    return f'<!doctype html><title>Upload new File</title><h1>Upload new File</h1><form method=post enctype=multipart/form-data><input type=file name=file><input type=submit value=Upload></form><a href="{url_for("fileupload.list")}">List of Files</a>'

@fileupload.route('/list', methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        pass
    else:
        stuff = ''
        for file in sorted(os.listdir(os.path.join(current_app.root_path, Serverconfig.get('fileuploadpath')))):
            href = url_for("fileupload.download", filename=file)
            print(href)
            stuff += f'<a href="{href}">{file}</a><br>'
        return f'<!doctype html><title>List of Files</title><a href="{url_for("fileupload.fileupload_")}">Upload files</a><hr><br>{stuff}'

@fileupload.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, Serverconfig.get('fileuploadpath'))
    return send_from_directory(path=uploads, directory=uploads, filename=filename)


"""
@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)
"""
