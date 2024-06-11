import os
from flask import Blueprint, render_template, request
import config
import requests
import json
import zipfile

from auth import auth
app = Blueprint('market', __name__)
appearance = config.get_config("appearance")
install_path = config.get_config("server", "path")
registry = config.get_config("market", "registry")

@app.route('/')
def apps():
    if auth() == False:
        return render_template('login.html')
    if config.get_config("market", "app_registry") == None:
        try:
            response = requests.get(registry+"apps.json")
        except requests.exceptions.ConnectTimeout:
            return render_template('error/index.html', error = "源出错。错误信息：<br>"+response.text,appearance=appearance)
    else:
        try:
            response = requests.get(config.get_config("market", "app_registry"))
        except requests.exceptions.ConnectTimeout:
            return render_template('error/index.html', error = "源出错。错误信息：<br>"+response.text,appearance=appearance)
    plugin_list = json.loads(response.text)
    return render_template('market/apps.html', plugin_list = plugin_list,appearance=appearance)

@app.route('/theme')
def theme():
    if auth() == False:
        return render_template('login.html')
    response = requests.get(registry+"theme.json")
    theme_list = json.loads(response.text)
    return render_template('market/theme.html', theme_list = theme_list,appearance=appearance)

@app.route('/install/theme/<url>')
def install_theme(url):
    if auth() == False:
        return render_template('login.html')
    response = requests.get(url)
    temp_path = install_path+"temp/theme.zip"
    save_path = install_path+"templates/resource/style/", "wb"
    with open(temp_path, "wb") as f:
        f.write(response.text)
        file=zipfile.ZipFile(temp_path)
        file.extractall(save_path)
        file.close()
    return "安装成功！"

@app.route('/install/plugin/<url>')
def install_plugin(url):
    if auth() == False:
        return render_template('login.html')
    response = requests.get(url)
    temp_path = +"temp/plugin.py"
    with open(temp_path, "w") as f:
        f.write(response.text)
    os.system("python "+temp_path+" "+install_path)
    return "安装成功！"