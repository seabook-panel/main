from flask import Flask,render_template,request,after_this_request
from auth import auth
import config
import platform
import function
from route import website,account,settings,market,files

app = Flask(__name__, static_folder="templates",static_url_path='')
app.register_blueprint(website.app, url_prefix='/website')
app.register_blueprint(account.app, url_prefix='/account')
app.register_blueprint(settings.app, url_prefix='/settings')
app.register_blueprint(market.app, url_prefix='/market')
app.register_blueprint(files.app, url_prefix='/files')
app.config['HOST'] = config.get_config("server", "host")
app.config['PORT'] = config.get_config("server", "port")

appearance = config.get_config("appearance")

@app.route('/')
def home():
    if auth() == False:
        return render_template('login.html')
    hostname = str(platform.node())
    local_ip = str(function.local_ip())
    external_ip = str(function.external_ip())
    info = {
        'platform': str(platform.platform()),
        'hostname': hostname,
        'ip': [local_ip,external_ip],
        'memory': {
            'used': str(function.memory_used())
        },
        'cpu': {
            'used':str(function.cpu_percent()),
            'core_number':{
                "core": str(function.cpu_count_core())},
                "logical": str(function.cpu_count_logical())
        }
    }
    return render_template('index.html',info=info,appearance=appearance)

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
        return render_template('power/shutdown.html',appearance=appearance)

if __name__ == '__main__':
    mode = config.get_config("server", "mode")
    if mode == "Debug" or mode == "debug":
        app.run(host=app.config['HOST'],port=app.config['PORT'],debug=True)
    else:
        print("哎呀！出错啦！")
        print("您未开启Debug模式，请使用WSGI运行。")