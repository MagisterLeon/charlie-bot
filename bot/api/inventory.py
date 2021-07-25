import os
import sys

from flask import request, Blueprint, current_app, redirect, url_for
from werkzeug.utils import secure_filename

bp = Blueprint("inventory", __name__)


@bp.route('/inventory', methods=['POST'])
def upload_inventory():
    file = request.files['file']
    filename = secure_filename(file.filename)
    folder = current_app.config['UPLOAD_FOLDER']

    print(f"Uploading inventory file: {filename} to folder: {folder}", file=sys.stdout)
    file.save(os.path.join(folder, filename))
    print(f"Inventory: {filename} uploaded successfully", file=sys.stdout)

    return redirect(url_for('home'))

