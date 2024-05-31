import toml
import os
import hashlib

path = os.getcwd() + "\\config.toml"
def get_admin_password():
    config = toml.load(path)
    password = config['admin']['password']
    if config['admin']['password_hash'] == "False":
        hash_password = hashlib.sha256(password.encode()).hexdigest()
        return hash_password
    else:
        return password
    
def set_admin_password(password):
    config = toml.load(path)
    config['admin']['password'] = password
    config['admin']['password_hash'] = "True"
    with open(path, 'w') as f:
        toml.dump(config, f)
    return