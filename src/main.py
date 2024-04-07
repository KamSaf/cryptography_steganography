from flask import Flask, render_template, request, flash
from utils import save_file
import os
from steganography import create_image, decode_image
from caesar import CaesarCipher as cs
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = '6l0YPaxzcmwZNcSK0PjLb9FSRviHCa8f'

UPLOAD_FOLDER = os.path.dirname(__file__) + os.path.join('/static/images/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def root():
    return render_template('index.html')


@app.route("/encode", methods=["GET", "POST"])
def encode():
    if request.method == 'POST':
        filename = save_file(request=request) if request.method == 'POST' else None
        message = request.form.get('frm_message')
        if not message:
            flash('No message to hide given.')
            return render_template('encode.html')

        if filename and message:
            shift = randint(3, 9)
            encrypted_message = cs.cipher(text=message, shift=shift) + str(shift)
            path = UPLOAD_FOLDER + filename
            create_image(message=encrypted_message, input_file=path, output_file=path)
            return render_template(template_name_or_list='encode.html', filename='images/' + filename)
    return render_template('encode.html')


@app.route("/decode", methods=["GET", "POST"])
def decode():
    if request.method == 'POST':
        filename = save_file(request=request) if request.method == 'POST' else None

        if filename:
            path = UPLOAD_FOLDER + filename
            hidden_message = decode_image(input_file=path)
            decrypted_message = ''
            try:
                decrypted_message = cs.decipher(text=hidden_message[:-1], shift=int(hidden_message[-1]))
            except Exception:
                flash('Message not found')
            return render_template(template_name_or_list='decode.html', message=decrypted_message)
    return render_template('decode.html')


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
