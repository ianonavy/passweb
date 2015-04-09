# Tread with caution
# This code was writen in 15 minutes

from flask import Flask, request, url_for, render_template, redirect
from flask.ext.login import login_required, LoginManager, login_user, \
    logout_user, session, abort
import base64
import os
import subprocess

app = Flask(__name__)
with open('secret.txt') as secret:
    app.config['SECRET_KEY'] = secret.read()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = base64.b64encode(os.urandom(16)).decode('utf-8')
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token



class User(object):
    """Dummy user class for flask-login"""

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return 'admin'


@login_manager.user_loader
def load_user(userid):
    return User()


def get_pass(name):
    ret = subprocess.check_output(
        "pass {} | head -n1".format(name), shell=True)
    return ret[:-1].decode('utf-8')  # strip newline


@app.route('/password/')
@login_required
def password():
    name = request.args.get('name', 'ls')
    return subprocess.check_output(
        "pass {}".format(name),
        shell=True).decode('utf-8').replace('\n', '<br />')


@app.route('/')
@login_required
def index():
    names = subprocess.check_output("pass ls", shell=True).decode('utf-8').split('\n')

    # hack to parse out of 'pass ls' into URLs
    prefix = []  # directory stack
    for i, name in enumerate(names):
        if '[01;34m' in name:  # directory detected by the color escapes... ugh
            # strip color sequences and ESC character
            name = name.replace('[01;34m', '').replace('[00m', '').replace('\x1b', '')
            names[i] = name  # store in original output
            _, name = name.rsplit("── ")  # parse out the name of the directory
            prefix.append(name.strip())  # add to list
        else:
            if "── " in name:
                _, part_to_urlify = name.split("── ")  # parse out name
                # build the full name with all the directories
                get_param = "/".join(prefix) + "/" + part_to_urlify
                # get the URL for displaying the password
                url = url_for('password', name=get_param)
                # hot swap it in with an anchor tag... so clean!
                names[i] = name.replace(
                    part_to_urlify,
                    "<a href='{}'>{}</a>".format(url, part_to_urlify))
            if "└" in name and prefix:  # last thing in directory
                prefix.pop()  # go up one level
    return render_template('index.html', names=names)


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if request.form['password'] == get_pass('passweb'):
            login_user(User())
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html")


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0', debug=False, ssl_context=('passweb.crt', 'passweb.key'))
