from flask import Blueprint, render_template, g, current_app, request, session, g, redirect, url_for, abort
from sqlite3 import dbapi2 as sqlite3

bp = Blueprint('usermanager', __name__)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(current_app.config['USER_DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@bp.route('/users')
def show_users():
    db = get_db()
    # select e_id
    cur = db.execute('SELECT uid, username, password FROM users ORDER BY uid DESC')
    users = cur.fetchall()
    return render_template('show_users.html', entries=users)


@bp.route('/register', methods=['POST'])
def add_user():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)',
               [request.form['username'], request.form['password']])
    db.commit()
    return redirect(url_for('usermanager.show_users'))


@bp.route('/delete_user', methods=['POST'])
def delete_user():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('DELETE FROM users WHERE uid=(?)', [request.args.get('eid')])
    db.commit()
    return redirect(url_for('usermanager.show_users'))


@bp.route('/update_user', methods=['POST'])
def update_user():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('UPDATE users SET username=(?),password=(?) WHERE uid=(?)',
               [request.form['username'], request.form['password'], request.form['uid']])
    db.commit()
    return redirect(url_for('usermanager.show_users'))

# @bp.route('/gotoupdate',methods=['POST'])
# def gotoupdate():
#     db = get_db()
#     cur = db.execute('select e_id,title,text from entries where e_id=(?)',[request.args.get('eid')])
#     e1 = cur.fetchone()
#     return render_template('update_entries.html', entry=e1)
