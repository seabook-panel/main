import hashlib
from flask import Blueprint, render_template, request, make_response, redirect
from auth import auth
import config
app = Blueprint('settings', __name__)

appearance_settings = config.get_config('appearance')
settings_vaule = config.get_config()

@app.route('/',methods=['GET'])
@auth
def home():
    return render_template('settings/index.html',appearance=appearance_settings,setings=settings_vaule)

@app.route('/appearance',methods=['GET'])
@auth
def appearance():
    return render_template('settings/appearance.html',appearance=appearance_settings,setings=settings_vaule)

@app.route('/security',methods=['GET'])
@auth
def security():
    return render_template('settings/security.html',appearance=appearance_settings,setings=settings_vaule)

@app.route('/change/user',methods=['POST','GET'])
@auth
def change_user():
    password = request.form.get("password", type=str, default=None)
    if password != None:
        password = hashlib.sha256(password.encode()).hexdigest()
        config.set_account_password(password)
    return redirect('/account/logout')

@app.route('/change/panel',methods=['POST','GET'])
@auth
def change_panel():
    host = request.form.get("host", type=str, default=None)
    port = request.form.get("port", type=str, default=None)
    if port != None:
        config.set_config("server", "port", port)
    if host != None:
        config.set_config("server", "host", host)
    return redirect('/settings')

@app.route('/change/appearance',methods=['POST','GET'])
@auth
def change_appearance():
    theme = request.form.get("theme", type=str, default=None)
    if theme != None:
        config.set_config("appearance", "theme", theme)
    return redirect('/settings')