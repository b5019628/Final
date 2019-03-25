from flask import Flask, request, render_template_string, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name


@app.route('/hello-template-injection')
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