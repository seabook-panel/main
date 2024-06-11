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

@app.route('/<path:path>')
def path(path):
    if auth() == False:
        return render_template('login.html')
    return render_template('files/index.html', path=path, appearance=appearance)