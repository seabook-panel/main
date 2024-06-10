from flask import Blueprint, render_template, request
import config


from auth import auth
app = Blueprint('files', __name__)
appearance = config.get_config("appearance")

@app.route('/')
def index():
    if auth() == False:
        return render_template('login.html')
    return render_template('files/index.html',appearance=appearance)