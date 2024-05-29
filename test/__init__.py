from flask import Flask, abort, render_template
import os

app = Flask(__name__)

# 假设所有HTML文件都在'templates'文件夹内
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_html_pages(filename):
    # 检查请求的路径是否以'/'结尾，如果是，则添加'index.html'
    if filename.endswith('/'):
        filename += 'index.html'

    return render_template(filename)

if __name__ == '__main__':
    app.run(debug=True,port=80)