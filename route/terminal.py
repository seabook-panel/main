from flask import Blueprint, render_template, redirect, request
import config


from auth import auth
app = Blueprint('terminal', __name__)
appearance = config.get_config("appearance")

@app.route('/')
@auth
def index():
    return "此功能暂未开发完毕。"