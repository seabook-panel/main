from flask import request
import config

def auth():
    seabook_password = request.cookies.get('seabook_password')
    if seabook_password != config.get_login_info():
        return False