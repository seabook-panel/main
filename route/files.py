from concurrent.futures import ThreadPoolExecutor
import concurrent
import os
import psutil
from flask import Blueprint, render_template, redirect, request
import config
import platform

from auth import auth
app = Blueprint('files', __name__)
appearance = config.get_config("appearance")

@app.route('/')
@auth
def index():
    files = {
        "folders": [],
        "files": []
    }
    if platform.system() == "Windows":
        for i in psutil.disk_partitions():
            name = i.device.replace("\\", "")
            files['folders'].append({'name': name})
            print(i.device,type(i.device))
    elif platform.system() == "Linux":
        item_list = os.listdir("/")
        for item in item_list:
            full_path = os.path.join("/", item)
            if os.path.isdir(full_path):
                files['folders'].append({'name': item})
            if os.path.isfile(full_path):
                files['files'].append({'name': item,'path':full_path})
    return render_template('files/index.html', dir="/", files=files, appearance=appearance)

@app.route('/<path:dir>')
@auth
def path(dir):
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(os.path.isdir, os.path.join(dir, item)): item for item in os.listdir(dir)
        }
        files = {
            "folders": [], 
            "files": []
        }
        for future in concurrent.futures.as_completed(futures):
            item = futures[future]
            full_path = os.path.join(dir, item)
            is_dir = future.result()
            
            if is_dir:
                files['folders'].append({'name': item})
            else:
                files['files'].append({'name': item, 'path': full_path})

    return render_template('files/index.html', dir=dir, files=files, appearance=appearance)

@app.route('/edit/<path:dir>')
@auth
def edit(dir: str):
    with open(dir, "r", encoding='utf-8') as f:
        try:
            content = f.read()
        except UnicodeDecodeError as e:
            content = "暂时不能打开此文件。"
    edit_page = render_template('files/editor.html', dir=dir, content=content, appearance=appearance)
    return edit_page

@app.route('/edit_save/<path:dir>',methods=['POST'])
@auth
def edit_save(dir: str):
    with open(dir, "w", encoding='utf-8') as f:
        text = request.form['content']
        f.write(text.replace("\n", ""))
    return redirect("/files/edit/"+dir)