import os
from flask import Blueprint, render_template, redirect
import config
import requests
import json
import zipfile
import shutil

from auth import auth
app = Blueprint('market', __name__)
appearance = config.get_config("appearance")
install_path = config.get_config("server", "path")
registry = config.get_config("market", "registry")

@app.route('/')
@auth
def apps():
    if config.get_config("market", "app_registry") == None:
        try:
            response = requests.get(registry+"apps.json")
        except requests.exceptions.ConnectTimeout:
            return render_template('error/index.html', error = "源出错。错误信息："+response.text,appearance=appearance)
    else:
        try:
            response = requests.get(config.get_config("market", "app_registry"))
        except requests.exceptions.ConnectTimeout:
            return render_template('error/index.html', error = "源出错。错误信息："+response.text,appearance=appearance)
    plugin_list = json.loads(response.text)
    return render_template('market/apps.html', plugin_list = plugin_list,appearance=appearance)

@app.route('/theme')
@auth
def theme():
    response = requests.get(registry+"theme.json")
    theme_list = json.loads(response.text)
    return render_template('market/theme.html', theme_list = theme_list,appearance=appearance)

@app.route('/install/theme/<name>/<path:url>')
@auth
def install_theme(url, name):
    try:
        response = requests.get(url, timeout=100000)
    except Exception as e:
        return render_template('error/index.html', error="源出错。错误信息：<br>" + str(e), appearance=appearance)
    temp_path = install_path + "temp/theme.zip"
    save_path = install_path + "templates/resource/style/"
    with open(temp_path, "wb") as f:
        f.write(response.content)
    file = zipfile.ZipFile(temp_path)
    file.extractall(save_path)
    file.close()
    folder_name = file.namelist()[0]
    folder_name = folder_name.replace("/", "")
    target_name = name.decode('utf-8') if isinstance(name, bytes) else name
    target_path = os.path.join(save_path, target_name)
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    os.rename(os.path.join(save_path, folder_name), target_path)
    config.set_config("appearance", "theme", target_name)
    return redirect("/")

@app.route('/install/plugin/<path:url>')
@auth
def install_plugin(url):
    response = requests.get(url)
    temp_path = +"temp/plugin.py"
    with open(temp_path, "w") as f:
        f.write(response.text)
    os.system("python "+temp_path+" "+install_path)
    return "安装成功！"