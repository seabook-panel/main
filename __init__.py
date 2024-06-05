from flask import Flask, redirect,render_template,request,make_response,after_this_request
from auth import auth
import config
import hashlib
import platform
import function
from route import website

app = Flask(__name__, static_folder="templates",static_url_path='')
app.register_blueprint(website.app, url_prefix='/website')

@app.route('/')
def home():
    if auth() == False:
        return render_template('login.html')
    hostname = str(platform.node())
    local_ip = str(function.local_ip())
    external_ip = str(function.external_ip())
    memory_used = str(function.memory_used()).replace('GB', '')
    cpu_percent = str(function.cpu_percent())
    info = {
        'platform': str(platform.platform()),
        'hostname': hostname,
        'ip': [local_ip,external_ip],
        'memory': memory_used,
        'cpu': cpu_percent
    }
    return render_template('index.html',info=info)

@app.route('/power/<name>')
def power(name):
    if auth() == False:
        return render_template('login.html')
    if name == "reboot":
        @after_this_request
        def reboot(response):
            function.reboot()
            print("IP地址为"+request.remote_addr+"的管理员重启了服务器。")
            return response
        return render_template('power/reboot.html')
    if name == "shutdown":
        @after_this_request
        def shutdown(response):
            function.shutdown()
            print("IP地址为"+request.remote_addr+"的管理员关闭了服务器。")
            return response
        return render_template('power/shutdown.html')

@app.route('/settings/')
def settings():
    if auth() == False:
        return render_template('login.html')
    return render_template('settings/index.html')

@app.route('/account/<name>',methods=['POST','GET'])
def account(name):
    if name == "login":
        resp = make_response(redirect('/'))
        password = request.form.get("password", type=str, default=None)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        resp.set_cookie("seabook_password", password_hash)
        print("IP地址为"+request.remote_addr+"的管理员登录了海书面板。")
        return resp
    if name == "logout":
        resp = make_response(redirect('/'))
        resp.delete_cookie("seabook_password")
        print("IP地址为"+request.remote_addr+"的管理员退出了海书面板。")
        return resp
    if name == "change_verify":
        if auth() == False:
            return render_template('login.html')
        password = request.form.get("password", type=str, default=None)
        if password != None:
            password = hashlib.sha256(password.encode()).hexdigest()
            config.set_admin_password(password)
        return redirect('/')

app.run(debug=True,host='0.0.0.0')