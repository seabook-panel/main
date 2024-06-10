from flask import Blueprint, render_template, request
import config
import requests
import json

from auth import auth
app = Blueprint('market', __name__)
appearance = config.get_config("appearance")

registry = "https://raw.githubusercontent.com/seabook-panel/market/main/registry/"

@app.route('/')
def apps():
    if auth() == False:
        return render_template('login.html')
    response = requests.get(registry+"apps.json")
    plugin_list = json.loads(response.text)
    return render_template('market/apps.html', plugin_list = plugin_list,appearance=appearance)

@app.route('/theme')
def theme():
    if auth() == False:
        return render_template('login.html')
    response = requests.get(registry+"theme.json")
    theme_list = json.loads(response.text)
    return render_template('market/theme.html', theme_list = theme_list,appearance=appearance)