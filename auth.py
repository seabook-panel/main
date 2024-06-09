import hashlib
from flask import request
import config

def auth():
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
        return False
    else:
        return True