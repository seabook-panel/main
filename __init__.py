from flask import Flask,render_template

app = Flask(__name__, static_folder="templates",static_url_path='')

@app.route('/')
def index():  
    return render_template('index.html')

app.run(debug=True)