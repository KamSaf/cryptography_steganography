from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/encode")
def encode():
    return render_template('encode.html')

@app.route("/decode")
def decode():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)