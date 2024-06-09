import hashlib
from flask import request
import toml
import os

path = os.getcwd() + '/config.toml'

def auth():
    verify_password = request.cookies.get('seabook_password')
    verify_username = request.cookies.get('seabook_username')
    config = toml.load(path)
    password = config['account']['password']
    username = config['account']['username']
    try:
        if config['account']['password_hash'] == "False":
            hash_password = hashlib.sha256(password.encode()).hexdigest()
            password = hash_password
    except KeyError:
        pass
    if verify_password != password or verify_username != username:
        return False