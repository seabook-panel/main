import toml
import os
import hashlib

path = os.getcwd() + "\\config.toml"
def get_admin_password():
    config = toml.load(path)
    password = config['admin']['password']
    if config['admin']['password_hash'] == "False":
        hash_password = hashlib.sha512(password.encode()).hexdigest()
        return hash_password
    else:
        return password