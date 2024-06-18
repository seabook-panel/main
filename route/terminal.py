from flask import Blueprint, render_template, request
import config
import os

from auth import auth
app = Blueprint('terminal', __name__)
appearance = config.get_config("appearance")

@app.route('/')
@auth
def index():
    return render_template("terminal/index.html",appearance=appearance)

@app.route('/run',methods=['GET', 'POST'])
@auth
def run():
    command = request.form.get('command')
    if "rm" in command:
        return "删除命令禁止使用。"
    elif "sudo" in command:
        return "sudo命令禁止使用。"
    command = str(command)
    output_lines = os.popen(command).readlines()
    clean_output = [line.strip() for line in output_lines if line.strip()]
    output = '\n'.join(clean_output)
    return output