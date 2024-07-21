from flask import Flask, request, redirect, url_for, render_template, Response
import os
import csv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# CHANGE ME (or use env. variables)
USERNAME = 'admin'
PASSWORD = 'password'


# Create the upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def parse_csv(filepath):
    items = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            items.append(row)
    return items

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    items = parse_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'items.csv'))
    return render_template('index.html', items=items)

@app.route('/upload', methods=['GET', 'POST'])
@requires_auth
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'items.csv')
            file.save(filepath)
            return redirect(url_for('index'))
    return '''
    <!doctype html>
    <title>Upload CSV</title>
    <h1>Upload new CSV</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
