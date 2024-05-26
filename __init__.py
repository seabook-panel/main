from flask import Flask,render_template
import subprocess
import platform

app = Flask(__name__, static_folder="templates",static_url_path='')

@app.route('/')
def index():  
    return render_template('index.html')

@app.route('/server/<name>')
def server(name):
    if name == None:
        return "</h1>海书面板提醒您：这里是用于控制服务器的重要区域，请不要主动访问。</h1>"
    if name == "reboot":
        if platform.system() == "Windows":
            subprocess.run(['shutdown', '/r', '/t', '0'])
        elif platform.system() == "Linux":
            subprocess.run(['reboot'])
        else:
            return "<h1>海书面板提醒您：目前不支持该操作系统。</h1>唉？这是什么奇怪的系统，快去反馈给我们吧！识别ID：" + platform.system()


app.run(debug=True)