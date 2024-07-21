from functools import wraps
from flask import Flask, request, redirect, url_for, render_template, Response, send_from_directory
from PIL import Image
import os
import csv
import re

# CHANGE ME (or use env. variables)
USERNAME = os.environ.get('GARAGE_SALE_USERNAME', 'admin')
PASSWORD = os.environ.get('GARAGE_SALE_PASSWORD', 'password')
VALID_STATUSES = {'Published', 'Reserved', 'Sold'}

IMAGE_SIZE = (500, 500)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['IMAGE_FOLDER'] = 'uploads/images'

# Create the upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def parse_csv(filepath):
    items = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Status'] in VALID_STATUSES:
                items.append(row)
    return items

def save_image(file, internal_id, image_number):
    img = Image.open(file)
    img.thumbnail((500, 500))
    img.save(os.path.join(app.config['IMAGE_FOLDER'], f'{internal_id}_{image_number}.jpg'))


def get_item_images():
    """Assumption: File format is <ID>_<nr>.jpg"""
    images = {}
    pattern = r"^(?P<name>.*?)_(?P<nr>\d+)\.jpg$"

    for filename in os.listdir(app.config['IMAGE_FOLDER']):
        match = re.match(pattern, filename)

        if match:
            internal_id = match.group("name")
            image_number = match.group("nr")

            if internal_id not in images:
                images[internal_id] = []
            images[internal_id].append(filename)

    return images


def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated



@app.route('/', endpoint='index')
def index():
    items = parse_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'items.csv'))
    images = get_item_images()
    return render_template('index.html', items=items, images=images)

@app.route('/admin', endpoint='admin')
@requires_auth
def admin():
    success = request.args.get('success', 0)
    images = sorted(os.listdir(app.config['IMAGE_FOLDER']))
    return render_template('upload.html', images=images, success=int(success))


@app.route('/admin/upload', methods=['POST'], endpoint='upload_file')
@requires_auth
def upload_file():
    files = request.files.getlist('file')
    for file in files:
        if file.filename.endswith('.csv'):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'items.csv'))
        elif file and '_' in file.filename:
            parts = file.filename.rsplit('_', 1)
            internal_id = parts[0]
            image_number = parts[1].split('.')[0]
            save_image(file, internal_id, image_number)
    return redirect(url_for('admin', success=1))

@app.route('/imgs/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, port=8000)
