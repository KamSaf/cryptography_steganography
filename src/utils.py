from flask import flash, Request
from flask import current_app as app
from werkzeug.utils import secure_filename
from datetime import datetime
import os

def allowed_file(filename):
    """
    """
    ALLOWED_EXTENSIONS = {'jpg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(request: Request) -> str:
    """
    """
    if 'frm_image' not in request.files or request.files['frm_image'].filename == '':
        flash('No file uploaded')
        return ''
    file = request.files['frm_image']
    if not allowed_file(file.filename):
        flash('Only .jpg format files can be uploaded.')
        return ''

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) if file.filename else 'file_' + datetime.now().strftime("%y%m%d_%H%M%S")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'temp/' + filename
    return ''