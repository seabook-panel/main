from flask import Flask,render_template,request,after_this_request
from auth import auth
import config
import platform
import function
from route import website,account

app = Flask(__name__, static_folder="templates",static_url_path='')
app.register_blueprint(website.app, url_prefix='/website')
app.register_blueprint(account.app, url_prefix='/account')
app.config['HOST'] = config.get_server_info()['host']
app.config['PORT'] = config.get_server_info()['port']

@app.route('/')
def home():
    if auth() == False:
        return render_template('login.html')
    hostname = str(platform.node())
    local_ip = str(function.local_ip())
    external_ip = str(function.external_ip())
    memory_used = str(function.memory_used())
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

if __name__ == '__main__':
    mode = config.get_server_info()['mode']
    if mode == "Debug" or mode == "debug":
        app.run(host=app.config['HOST'],port=app.config['PORT'],debug=True)
    else:
        print("哎呀！出错啦！")
        print("您未开启Debug模式，请使用WSGI运行。")