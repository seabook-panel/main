from flask import Flask, redirect,render_template,request,make_response
import requests
import config
import hashlib
import platform
import function
import os
import toml
import shutil

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
    memory_used = str(function.memory_used()).replace('GB', '')
    cpu_percent = str(function.cpu_percent())
    return render_template('index.html',poetry=poetry,platform=display_platform,hostname=hostname,local_ip=local_ip,external_ip=external_ip,memory_used=memory_used,cpu_percent=cpu_percent)

@app.route('/website/')
def website():
    return render_template('website/index.html',websites=toml.load('./website.toml'))

@app.route('/website/create',methods=['POST'])
def website_create():
    if auth() == False:
        return render_template('login.html')
    dir = request.form.get("dir", type=str, default=None)
    name = request.form.get("name", type=str, default=None)
    if dir[-1] != "/":
        dir = dir+"/"
    if "\\" in dir:
        dir = dir.replace("\\", "/")
    appdir=dir+name+"/"
    if os.path.exists(appdir) == False:
        os.mkdir(appdir)
    site_type = request.form.get("type", type=str, default=None)
    if site_type == "jinja2":
        with open(appdir+"__init__.py", "w") as f:
            jinja2_code = R"""from flask import Flask, abort, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_html_pages(filename):
    # 检查请求的路径是否以'/'结尾，如果是，则添加'index.html'
    if filename.endswith('/'):
        filename += 'index.html'

    return render_template(filename)

if __name__ == '__main__':
    app.run(debug=True,port="""+request.form.get("port", type=str, default=None)+""")"""
            f.write(jinja2_code)
        name = name.replace(" ", "")
        data = toml.load("website.toml")
        try:
            last_name = next(iter(data.keys()))
            last_id = data[last_name]["id"]
        except IndexError:
            last_id = 0
        toml.dump({name:{"id":int(last_id)+1,"name":name,"dir":dir,"type":"Jinja2","port":request.form.get("port", type=str, default=None)}}, open("website.toml", "a"))
        return "<h1>海书面板提醒您：已创建网站，位于目录"+dir+"</h1>"

@app.route('/website/delete/<id>')
def website_delete(id):
    if auth() == False:
        return render_template('login.html')
    website_config = toml.load("website.toml")
    if id in website_config:
        shutil.rmtree(website_config[id]["dir"])
        del website_config[id]
        toml.dump(website_config, open("website.toml", "w"))
        return "<h1>海书面板提醒您：已删除网站"+id+"</h1>"
    else:
        return "<h1>网站"+id+"不存在。</h1>"

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
    if name == "shutdown":
        function.shutdown()

@app.route('/settings/')
def settings():
    if auth() == False:
        return render_template('login.html')
    return render_template('settings/index.html')

@app.route('/account/<name>',methods=['POST'])
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
        if password == None:
            password = config.get_admin_password()
        else:
            password = hashlib.sha256(password.encode()).hexdigest()
        config.set_admin_password(password)
        return redirect('/')

app.run(debug=True,host='0.0.0.0')