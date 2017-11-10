
from flask import Blueprint, render_template,g,current_app, request, session, g, redirect, url_for, abort
from sqlite3 import dbapi2 as sqlite3
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

@bp.route('/')
def show_entries():
    db = get_db()
    # select e_id
    cur = db.execute('select e_id, title, text from entries order by e_id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@bp.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    return redirect(url_for('dbmanager.show_entries'))

@bp.route('/delete', methods=['POST'])
def delete_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from entries where e_id=(?)',[request.args.get('eid')])
    db.commit()
    return redirect(url_for('dbmanager.show_entries'))

@bp.route('/update', methods=['POST'])
def update_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('update entries set title=(?),text=(?) where e_id=(?)',
               [request.form['title'], request.form['text'],request.form['eid']])
    db.commit()
    return redirect(url_for('dbmanager.show_entries'))

@bp.route('/gotoupdate',methods=['POST'])
def gotoupdate():
    db = get_db()
    cur = db.execute('select e_id,title,text from entries where e_id=(?)',[request.args.get('eid')])
    e1 = cur.fetchone()
    return render_template('update_entries.html', entry=e1)


