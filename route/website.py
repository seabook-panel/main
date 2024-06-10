from flask import Blueprint, render_template, request
import toml
import os
import shutil
from multiprocessing import Process
import config


from auth import auth
app = Blueprint('website', __name__)
appearance = config.get_config("appearance")

@app.route('/')
def index():
    if auth() == False:
        return render_template('login.html')
    return render_template('website/index.html',websites=toml.load('./website.toml'),appearance=appearance)

@app.route('/create',methods=['POST'])
def create():
    website_jinja2_code = R"""from flask import Flask, abort, render_template
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
    app.run(debug=True,port=)"""
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
        with open(appdir+"__init__.py", "w",encoding="utf-8") as f:
            jinja2_code = website_jinja2_code.replace("port=", "port="+request.form.get("port", type=str, default=None))
            f.write(jinja2_code)
        name = name.replace(" ", "")
        data = toml.load("website.toml")
        try:
            last_id = next(iter(data.keys()))
        except IndexError:
            last_id = 0
        except StopIteration:
            last_id = 0
        except KeyError:
            last_id = 0
        new_website = {
            str(int(last_id)+1):{
                "name":name,
                "dir":appdir,
                "type":site_type,
                "host":request.form.get("host", type=str, default=None),
                "port":request.form.get("port", type=str, default=None)
                }
            }
        
        toml.dump(new_website, open("website.toml", "a"))
        return "<h1>海书面板提醒您：已创建网站，位于目录"+dir+"</h1>"

@app.route('/start/<id>')
def start(id):
    if auth() == False:
        return render_template('login.html')
    website_config = toml.load("website.toml")
    if id in website_config:
        with open(website_config[id]["dir"]+"run.bat", "w") as f:
            run_code = """@echo off
cd """+website_config[id]["dir"]+"""
flask --app __init__ run"""
            f.write(run_code)
        output = Process(target=os.system,args=("powershell "+website_config[id]["dir"]+"run.bat",))
        output.start()
        print(output)

    return "<h1>海书面板提醒您：已启动网站"+id+"</h1>"

@app.route('/delete/<id>')
def delete(id):
    if auth() == False:
        return render_template('login.html')
    website_config = toml.load("website.toml")
    if id in website_config:
        shutil.rmtree(website_config[id]["dir"])
        del website_config[id]
        with open("website.toml", "w") as f:
            toml.dump(website_config, f)
        return "<h1>海书面板提醒您：已删除网站"+id+"</h1>"
    else:
        return "<h1>网站"+id+"不存在。</h1>"