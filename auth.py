import hashlib
from flask import request, render_template
import config
from functools import wraps

appearance = config.get_config("appearance")

def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_password = request.cookies.get('seabook_password')
        verify_username = request.cookies.get('seabook_username')
        password = config.get_config('account', 'password')
        username = config.get_config('account', 'username')
        try:
            if config.get_config('account', 'password_hash') == "False":
                hash_password = hashlib.sha256(password.encode()).hexdigest()
                password = hash_password
        except KeyError:
            pass
        if verify_password != password or verify_username != username:
            return render_template('login.html', appearance=appearance)
        else:
            return func(*args, **kwargs)  # 已登录
    return wrapper