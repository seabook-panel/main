import os
from flask import Blueprint, render_template, redirect
import config


from auth import auth
app = Blueprint('files', __name__)
appearance = config.get_config("appearance")

@app.route('/')
def index():
    if auth() == False:
        return render_template('login.html')
    return redirect('/files/'+config.get_config("server", "path"))

@app.route('/<path:dir>')
def path(dir):
    if auth() == False:
        return render_template('login.html')
    files = {
        "folders": [],
        "files": []
    }
    item_list = os.listdir(dir)
    for item in item_list:
        full_path = os.path.join(dir, item)
        if os.path.isdir(full_path):
            files['folders'].append({'name': item})
        if os.path.isfile(full_path):
            files['files'].append({'name': item})
    print(files)
    return render_template('files/index.html', dir=dir, files=files, appearance=appearance)