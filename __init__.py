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
    poetry = str(poetry.content,'utf-8')
    display_platform = str(platform.platform())
    hostname = str(platform.node())
    local_ip = str(function.local_ip())
    external_ip = str(function.external_ip())
    memory_totol = str(function.memory_totol())
    memory_used = str(function.memory_used())
    memory_free = str(function.memory_free())
    cpu_count_main = str(function.cpu_count_main())
    cpu_count_logical = str(function.cpu_count_logical())
    cpu_freq = str(function.cpu_freq()) + "GHz"
    cpu_percent = str(function.cpu_percent()) + "%"
    return render_template('index.html',poetry=poetry,platform=display_platform,hostname=hostname,local_ip=local_ip,external_ip=external_ip,memory_totol=memory_totol,memory_used=memory_used,memory_free=memory_free,cpu_count_main=cpu_count_main,cpu_count_logical=cpu_count_logical,cpu_freq=cpu_freq,cpu_percent=cpu_percent)

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

app.run(debug=True,host='0.0.0.0')