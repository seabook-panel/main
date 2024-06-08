import asyncio
from flask import Flask, abort, render_template
import os

app = Flask(__name__)

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
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.run()