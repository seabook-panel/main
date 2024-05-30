from flask import Flask, abort, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_html_pages(filename):
    # ��������·���Ƿ���'/'��β������ǣ������'index.html'
    if filename.endswith('/'):
        filename += 'index.html'

    return render_template(filename)

if __name__ == '__main__':
    app.run(debug=True,port=8080)