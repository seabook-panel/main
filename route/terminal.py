from flask import Blueprint, render_template, render_template_string, request
import config
import subprocess

from auth import auth
app = Blueprint('terminal', __name__)
appearance = config.get_config("appearance")

@app.route('/')
@auth
def index():
    htme_string = """
<form action="./run" method="POST">
<input type="text" name="command" placeholder="输入命令">
<input type="submit" value="执行">
"""
    return render_template_string(htme_string)

@app.route('/run',methods=['GET', 'POST'])
@auth
def run():
    command = request.form.get('command')
    if "rm" in command:
        return "删除命令禁止使用。"
    elif "sudo" in command:
        return "sudo命令禁止使用。"
    command = str(command)
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return output.stdout