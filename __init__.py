from flask import Flask,render_template

app = Flask(__name__, static_folder="templates",static_url_path='')

@app.route('/')
def index():  
    return render_template('index.html')

@app.route('/server/')
def server_waring():
    return "</h1>海书面板提醒您：这里是用于控制服务器的重要区域，请不要主动访问。</h1>"

@app.route('/server/<name>')
def server(name):
    if name == None:
        return "</h1>海书面板提醒您：这里是用于控制服务器的重要区域，请不要主动访问。</h1>"
    if name == "reboot":
        import reboot
        reboot.reboot()


app.run(debug=True)