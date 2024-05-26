from flask import Flask, redirect,render_template,request,make_response
import requests
import config
import hashlib
import platform
import function

def auth():
    seabook_password = request.cookies.get('seabook_password')
    if seabook_password != config.get_admin_password():
        return False

app = Flask(__name__, static_folder="templates",static_url_path='')

@app.route('/')
def home():
    if auth() == False:
        return render_template('login.html')
    poetry = requests.get('https://xinghaiapi.pythonanywhere.com/poetry-moment/get/text')
    return render_template('index.html',poetry=str(poetry.content,'utf-8'),platform=str(platform.platform()),hostname=str(platform.node()),ip=str())

@app.route('/server/')
def server_waring():
    return "</h1>海书面板提醒您：这里是用于控制服务器的重要区域，请不要主动访问。</h1>"

@app.route('/server/<name>')
def server(name):
    if auth() == False:
        return render_template('login.html')
    if name == None:
        return "</h1>海书面板提醒您：这里是用于控制服务器的重要区域，请不要主动访问。</h1>"
    if name == "reboot":
        function.reboot()

@app.route('/login/',methods=['POST'])
def login():
    resp = make_response(redirect('/'))
    password = request.form.get("password", type=str, default=None)
    password_hash = hashlib.sha512(password.encode()).hexdigest()
    resp.set_cookie("seabook_password", password_hash)
    return resp
app.run(debug=True)