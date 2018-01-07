import flask
from werkzeug.utils import find_modules, import_string
import os
import flask_login as fl
import sqlite3

# from  wtforms import *

bp = flask.Blueprint('usermanager', __name__)
app = flask.Flask(__name__)
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'entries.sqlite'),
    USER_DATABASE=os.path.join(app.root_path, 'users.sqlite'),
    DEBUG = True,
    SECRET_KEY = '123456',
))

login_manager = fl.LoginManager()
login_manager.init_app(app)


# Mock database, change to sqlite later
# users = {'foo@bar.tld': {'password': 'hi'}}

class User(fl.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    user = query_db('select * from users where username = ?',
                    [username], one=True)
    if user is None:
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    the_user = query_db('select * from users where username = ?',
                        [username], one=True)
    if the_user is None:
        return

    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!

    if request.form['password'] != the_user[2]:
        return
    # user.is_authenticated = (request.form['password'] == the_user[2])

    return user


def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = sqlite3.connect(flask.current_app.config['USER_DATABASE'])
    return db
    db.row_factory = sqlite3.Row


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if flask.request.method == 'POST':
        the_username = flask.request.form['username']
        the_password = flask.request.form['password']
        user = query_db('select * from users where username = ?',
                        [the_username], one=True)
        print(user)
        if user is not None:
            error = 'Username already exist'
        else:
            db = get_db()
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', [the_username, the_password])
            db.commit()
            user = User()
            user.id = the_username
            fl.login_user(user)
            flask.flash(user.id)
            flask.flash("success!")
            return flask.redirect(flask.url_for('dbmanager.show_entries'))
    return flask.render_template('register.html', error=error)


@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if flask.request.method == 'POST':
        the_username = flask.request.form['username']
        the_password = flask.request.form['password']
        user = query_db('select * from users where username = ?',
                        [the_username], one=True)
        if user is None:
            error = 'No such user'
        elif user[2] != the_password:
            error = 'Incorrect username or password'
        else:
            user = User()
            user.id = the_username
            fl.login_user(user)
            return flask.redirect(flask.url_for('dbmanager.show_entries'))
    return flask.render_template('login.html', error=error)


@app.route('/logout')
@fl.login_required
def logout():
    fl.logout_user()
    flask.flash('You were logged out')
    return flask.redirect(flask.url_for('login'))

def register_blueprints(app):
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None
register_blueprints(app)

# @app.route('/show_entries')
# @fl.login_required
# def show_entries():
#     return flask.render_template('show_entries.html')

if __name__ == '__main__':
    app.run(debug=True)