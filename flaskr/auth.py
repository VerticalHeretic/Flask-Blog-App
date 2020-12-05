import functools

from flask import ( Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.models import User,db
from flask_login import login_user,logout_user,login_required

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.session.query(User).filter(User.username == username).count() != 0:
            error = f'User {username} is already registered.'

        if error is None:
            data = User(username, generate_password_hash(password))
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            login_user(user)
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

