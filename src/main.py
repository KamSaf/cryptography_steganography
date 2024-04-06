from flask import Flask, render_template, request
from utils import *
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '6l0YPaxzcmwZNcSK0PjLb9FSRviHCa8f'

UPLOAD_FOLDER = os.path.join('static/temp/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route("/", methods=["GET"])
def root():
    return render_template('index.html')

@app.route("/encode", methods=["GET", "POST"])
def encode():
    if request.method == 'POST':
        filename = save_file(request=request) if request.method == 'POST' else None
        if filename:
            return render_template(template_name_or_list='encode.html', filename=filename)
    return render_template('encode.html')

@app.route("/decode", methods=["GET", "POST"])
def decode():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
