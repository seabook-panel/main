import toml
import os
path = os.getcwd() + "\\config.toml"

def set_config(group, key, value):
    config = toml.load(path)
    config[group][key] = value
    with open(path, 'w') as f:
        toml.dump(config, f)
    return

def get_config(group, key=None):
    config = toml.load(path)
    if key == None:
        vaule = config[group]
    else:
        vaule = config[group][key]
    return vaule

def set_account_password(password):
    config = toml.load(path)
    config['account']['password'] = password
    config['account']['password_hash'] = "True"
    with open(path, 'w') as f:
        toml.dump(config, f)
    return