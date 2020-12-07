
"""
This file serves double duty, it will contains the application factory, and it tells Python
that the flaskr directory should be treated as a package
"""

import os

from flask import Flask, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flaskr.models import User, db
from flask_wtf import CSRFProtect

csrf = CSRFProtect()

def create_app(test_config=None):
    # create and configure the app 
    app = Flask(__name__, instance_relative_config=True)

    ENV = 'dev'

    if ENV == 'dev':
        app.debug = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nimda@localhost/blog'
    else:
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vamlkhujptmgtc:219869fd4af80477550a1d47cb1fbefa1bc62eb3a922c2c927761ce63a582226@ec2-54-163-47-62.compute-1.amazonaws.com:5432/d7u95b7c4klkag'

    app.config.from_mapping(
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SECRET_KEY='dev'
    )

    # Here we enable CSRF protection for our app
    csrf.init_app(app)

    # Here we initalize db with app, this make is more abstract and give us a better flexibility in package
    db.init_app(app)
    # We add Flask Migrate for easyer work on database
    migrate = Migrate(app,db)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # This associate user cookie with user model id
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in 
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return "Hello, World!"


    # Blueprints section
    from flaskr.auth import auth
    app.register_blueprint(auth)

    from flaskr.blog import blog
    app.register_blueprint(blog)
    app.add_url_rule("/", endpoint='index')

    return app