from flask import Flask,make_response,redirect,abort,g,render_template,request,session,flash,url_for
from werkzeug.utils import find_modules, import_string
import os
app = Flask(__name__)
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'entries.sqlite'),
    DEBUG = True,
    SECRET_KEY = '123456',
    USERNAME = 'admin',
    PASSWORD = 'default'
))


@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            # return render_template('show_entries.html')
            return redirect(url_for('dbmanager.show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('dbmanager.show_entries'))

def register_blueprints(app):
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None
register_blueprints(app)

@app.route('/show_entries')
def show_entries():
    return render_template('show_entries.html')

if __name__ == '__main__':
    app.run(debug=True)