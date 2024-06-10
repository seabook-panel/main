from flask import Blueprint, render_template, request
import config
import requests
import json

from auth import auth
app = Blueprint('market', __name__)
appearance = config.get_config("appearance")

registry = "https://raw.githubusercontent.com/seabook-panel/market/main/registry/"
@app.route('/')
def index():
    if auth() == False:
        return render_template('login.html')
    response = requests.get(registry+"plugins.json")
    plugin_list = json.loads(response.text)
    return render_template('market/plugins.html', plugin_list = plugin_list,appearance=appearance)