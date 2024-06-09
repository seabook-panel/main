import hashlib
from flask import Blueprint, render_template, request, make_response, redirect
from auth import auth
import config
app = Blueprint('settings', __name__)


@app.route('/',methods=['GET'])
def home():
    if auth() == False:
        return render_template('login.html')
    return render_template('settings/index.html')

@app.route('/appearance',methods=['GET'])
def appearance():
    if auth() == False:
        return render_template('login.html')
    return render_template('settings/appearance.html')

@app.route('/security',methods=['GET'])
def security():
    if auth() == False:
        return render_template('login.html')
    return render_template('settings/security.html')

@app.route('/change/user',methods=['POST','GET'])
def change_user():
    if auth() == False:
        return render_template('login.html')
    password = request.form.get("password", type=str, default=None)
    if password != None:
        password = hashlib.sha256(password.encode()).hexdigest()
        config.set_account_password(password)
    return redirect('/')

@app.route('/change/panel',methods=['POST','GET'])
def change_panel():
    if auth() == False:
        return render_template('login.html')
    host = request.form.get("host", type=str, default=None)
    port = request.form.get("port", type=str, default=None)
    if port != None:
        config.set_config("server", "port", port)
    if host != None:
        config.set_config("server", "host", host)
    return redirect('/settings')