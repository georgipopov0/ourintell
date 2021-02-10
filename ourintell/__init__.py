import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from ourintell.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()


def create_app(test_config=None,config_class=Config):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config) 

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

    # initialise the database
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db_session.remove()
    
    # a simple page that says hello

    from ourintell.intell.routes import intell
    from ourintell.user.routes import user

    app.register_blueprint(intell)
    app.register_blueprint(user)

    print(app.config['MAIL_USERNAME'])
    print(app.config['MAIL_PASSWORD'])

    return app