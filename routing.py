from flask import Flask, flash, request, render_template_string, render_template, redirect, session, url_for
from flask_basicauth import BasicAuth
from flask_httpauth import HTTPBasicAuth
from werkzeug import secure_filename
from flask_autoindex import AutoIndex
import os
from functools import wraps


app = Flask(__name__)
auth = HTTPBasicAuth()
path = os.getcwd()+"\\templates\\upload\\"
list_of_files = {}
#UPLOAD_FOLDER = 'upload/'
#app.config['upload/'] = '/upload/'
#session['logged_in'] = False
app.secret_key = 'VerySecretKey'


users = {
    "admin": "books",
    "user": "donald"
}


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('landing'))
    return wrap


# Route for handling the landing page logic
@app.route('/', methods=['GET', 'POST'])
def landing():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'customer' or request.form['password'] != 'bookstore':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('landing.html', error=error)


@app.route('/upload')
@login_required
def upload():
        filepath = os.listdir(path )
        print(filepath)
        for filename in os.listdir(path):
            list_of_files[filename] = "http://localhost/"+filename
            return list_of_files[filename]


#@auth.get_password
#def get_pw(username):
#    if username in users:
#        return users.get(username)
#    return None





@app.route('/index')
@login_required
def home():
    return render_template('index.html')


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/admin2', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


# Route for handling the landing page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'test':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('admin'))
    return render_template('login.html', error=error)


@app.route('/child')
@login_required
def child():
    return render_template('child.html')


@app.route('/layout')
@login_required
def layout():
    return render_template('layout.html')


@app.route('/upload/<file>')
@login_required
def uploadfile(file):
   return render_template('/upload/' + file)


@app.route('/hello-template-injection')
@login_required
def hello_1():
    person = {'name': "world", 'secret': "UGhldmJoZj8gYWl2ZnZoei5wYnovcG5lcnJlZg=="}
    if request.args.get('name'):
        person['name'] = request.args.get('name')
    template = '''<h2>Hello %s!</h2>''' % person['name']
    return render_template_string(template, person=person)


####
# Private function if the user has local files.
###
def get_user_file(f_name):
    with open(f_name) as f:
        return f.readlines()


app.jinja_env.globals['get_user_file'] = get_user_file # Allows for use in Jinja2 templates


if __name__ == "__main__":
    app.run('localhost', '80', 'True',)