from flask import Blueprint, render_template, request, make_response, redirect
from auth import auth
import config
app = Blueprint('settings', __name__)


@app.route('/',methods=['GET'])
def home():
    if auth() == False:
        return render_template('login.html')
    return render_template('settings/index.html')

@app.route('/appearance',methods=['GET'])
def appearance():
    if auth() == False:
        return render_template('login.html')
    return render_template('settings/appearance.html')
