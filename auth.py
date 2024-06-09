import hashlib
from flask import request
import toml
import os

path = os.getcwd() + 'config.toml'

def auth():
    seabook_password = request.cookies.get('seabook_password')
    config = toml.load(path)
    password = config['account']['password']
    try:
        if config['account']['password_hash'] == "False":
            hash_password = hashlib.sha256(password.encode()).hexdigest()
            password = hash_password
    except KeyError:
        pass
    if seabook_password != password:
        return False