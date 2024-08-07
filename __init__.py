import xhlog as log
from flask import Flask,render_template
from auth import auth
import config
import platform
import function
from route import power,website,account,settings,market,files,terminal

app = Flask(__name__, static_folder="templates",static_url_path='')

app.register_blueprint(power.app, url_prefix='/power')
app.register_blueprint(website.app, url_prefix='/website')
app.register_blueprint(account.app, url_prefix='/account')
app.register_blueprint(settings.app, url_prefix='/settings')
app.register_blueprint(market.app, url_prefix='/market')
app.register_blueprint(files.app, url_prefix='/files')
app.register_blueprint(terminal.app, url_prefix='/terminal')
app.config['HOST'] = config.get_config("server", "host")
app.config['PORT'] = config.get_config("server", "port")

appearance = config.get_config("appearance")

@app.route('/')
@auth
def home():
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
                "core": str(function.cpu_count_core()),
                "logical": str(function.cpu_count_logical())
            }
        }
    }
    return render_template('home.html',info=info,appearance=appearance)

@app.errorhandler(404)
def error_404(e):
    return render_template('error/404.html',error=e,appearance=appearance), 404

@app.errorhandler(500)
def error_500(e):
    return render_template('error/500.html',error=e,appearance=appearance), 500

if __name__ == '__main__':
    mode = config.get_config("server", "mode")
    if mode == "Debug" or mode == "debug":
        app.run(host=app.config['HOST'],port=app.config['PORT'],debug=True)
    else:
        log.error("哎呀！出错啦！")
        log.error("您未开启Debug模式，请使用WSGI运行。",exit=True)