from concurrent.futures import ThreadPoolExecutor
import concurrent
import os
import psutil
from flask import Blueprint, render_template, redirect, request, send_file
import config
import platform

from auth import auth
app = Blueprint('files', __name__)
appearance = config.get_config("appearance")

@app.route('/')
@auth
def index_redirect():
    return redirect("/files/explorer/")

@app.route('/explorer/')
@auth
def index():
    files = {
        "folders": []
    }
    if platform.system() == "Windows":
        for i in psutil.disk_partitions():
            name = i.device.replace("\\", "")
            files['folders'].append({'name': name})
            print(i.device,type(i.device))
    elif platform.system() == "Linux":
        item_list = os.listdir("/")
        for item in item_list:
            files['folders'].append({'name': item})
    if platform.system() == "Windows":
        return render_template('files/root.html', dir="/", files=files, appearance=appearance)
    else:
        return render_template('files/index.html', dir="/", files=files, appearance=appearance)
    
@app.route('/explorer/<path:dir>')
@auth
def path(dir):
    try:
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
    except PermissionError:
        files = {
            "folders": [
                {
                    "name": "无权限"
                }
            ]
        }
    except FileNotFoundError:
        files = {
            "folders": [
                {
                    "name": "目录不存在"
                }
            ]
        }
    return render_template('files/index.html', dir=dir, files=files, appearance=appearance)

@app.route('/upload/<path:dir>', methods=['POST'])
@auth
def upload(dir: str):
    file = request.files['file']
    dir_file=os.path.join(dir, file.filename)
    file.save(dir_file)
    return redirect("/files/"+dir)

@app.route('/download/<path:dir>')
@auth
def downloads(dir: str):
    return send_file(dir, as_attachment=True)

@app.route('/edit/<path:dir>')
@auth
def edit(dir: str):
    with open(dir, "r", encoding='utf-8') as f:
        try:
            content = f.read()
        except UnicodeDecodeError as e:
            content = "暂时不能打开此文件。"
        except FileNotFoundError:
            content = "文件不存在。"
    edit_page = render_template('files/editor.html', dir=dir, content=content, appearance=appearance)
    return edit_page

@app.route('/edit_save/<path:dir>',methods=['POST'])
@auth
def edit_save(dir: str):
    text = request.form['content']
    if text == "暂时不能打开此文件。":
        return redirect("/files/edit/"+dir)
    with open(dir, "w", encoding='utf-8') as f:
        f.write(text.replace("\n", ""))
    return redirect("/files/edit/"+dir)