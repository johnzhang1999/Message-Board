from flask import Blueprint, render_template, current_app, request, session, g, redirect, url_for, abort
from sqlite3 import dbapi2 as sqlite3
import flask_login as fl
bp = Blueprint('dbmanager', __name__)
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@bp.route('/')
def show_entries():
    if fl.current_user.is_authenticated:
        entries = query_db('select * from entries where username = ?', [fl.current_user.id])
        # db = get_db()
        # # select e_id
        # cur = db.execute('select e_id, title, text from entries order by e_id desc')
        # entries = cur.fetchall()
        return render_template('show_entries.html', entries=entries)
    else:
        return render_template('please_login.html')

@bp.route('/add', methods=['POST'])
@fl.login_required
def add_entry():
    print(fl.current_user.get_id())
    db = get_db()
    db.execute('INSERT INTO entries (title, text, username) VALUES (?, ?, ?)',
               [request.form['title'], request.form['text'], fl.current_user.id])
    db.commit()
    return redirect(url_for('dbmanager.show_entries'))

@bp.route('/delete', methods=['POST'])
@fl.login_required
def delete_entry():

    db = get_db()
    db.execute('delete from entries where e_id=(?)',[request.args.get('eid')])
    db.commit()
    return redirect(url_for('dbmanager.show_entries'))

@bp.route('/update', methods=['POST'])
@fl.login_required
def update_entry():
    print([request.form['title'], request.form['text'], request.form['eid']])
    db = get_db()
    db.execute('update entries set title=(?),text=(?) where e_id=(?)',
               [request.form['title'], request.form['text'], request.form['eid']])
    db.commit()
    return redirect(url_for('dbmanager.show_entries'))

@bp.route('/gotoupdate',methods=['POST'])
@fl.login_required
def gotoupdate():
    db = get_db()
    cur = db.execute('select e_id,title,text from entries where e_id=(?)',[request.args.get('eid')])
    e1 = cur.fetchone()
    return render_template('update_entries.html', entry=e1)


