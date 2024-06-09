import hashlib
from flask import Blueprint, render_template, request, make_response, redirect
from auth import auth
import config
app = Blueprint('account', __name__)


@app.route('/login',methods=['POST','GET'])
def login():
    resp = make_response(redirect('/'))
    password = request.form.get("password", type=str, default=None)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    resp.set_cookie("seabook_password", password_hash)
    print("IP地址为"+request.remote_addr+"的管理员登录了海书面板。")
    return resp

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie("seabook_password")
    print("IP地址为"+request.remote_addr+"的管理员退出了海书面板。")
    return resp