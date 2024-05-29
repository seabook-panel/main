from flask import Flask, redirect,render_template,request,make_response
import requests
import config
import hashlib
import platform
import function
import os

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
def website_warn():
    return render_template('website/index.html')

@app.route('/website/create',methods=['POST'])
def website():
    if auth() == False:
        return render_template('login.html')
    dir = request.form.get("dir", type=str, default=None)
    if os.path.exists(dir) == False:
        os.mkdir(dir)
    if dir[-1] != "/":
        dir = dir+"/"
    if "\\" in dir:
        dir = dir.replace("\\", "/")
    site_type = request.form.get("type", type=str, default=None)
    if site_type == "jinja2":
        with open(dir+"__init__.py", "w") as f:
            jinja2_code = R"""from flask import Flask, abort, render_template
import os

app = Flask(__name__)

# 假设所有HTML文件都在'templates'文件夹内
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
    app.run(debug=True,port=80)
    """
            f.write(jinja2_code)
    return "<h1>海书面板提醒您：已创建网站，位于目录"+dir+"</h1>"

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

@app.route('/login/',methods=['POST'])
def login():
    resp = make_response(redirect('/'))
    password = request.form.get("password", type=str, default=None)
    password_hash = hashlib.sha512(password.encode()).hexdigest()
    resp.set_cookie("seabook_password", password_hash)
    print("IP地址为"+request.remote_addr+"的管理员登录了海书面板。")
    return resp

@app.route('/logout/')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie("seabook_password")
    print("IP地址为"+request.remote_addr+"的管理员退出了海书面板。")
    return resp

app.run(debug=True,host='0.0.0.0')