
from dotenv import load_dotenv
# load envrionment variables from '.env' file
load_dotenv()

from flask_login import user_logged_in, user_logged_out
from datetime import timedelta
from coinbase_commerce.client import Client
from flask_user import (UserManager, SQLAlchemyAdapter)
from config import config
from flask_babelex import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session
from flask_migrate import Migrate
import os



db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "user.login"
babel = Babel()
coinbase_client = Client(os.environ["COINBASE_APIKEY"])


def create_app(environment):
    def init_dependencies(app):
        from user import models

        login_manager.init_app(app)
        db.init_app(app)
        babel.init_app(app)


        # setup flask-user
        user_manager = UserManager(
             app, db, models.User, UserInvitationClass=models.UserInvitation)
        
        # use sendgrid for sending emails
        from flask_user.email_adapters import SendgridEmailAdapter
        user_manager.email_adapter = SendgridEmailAdapter(app)

    def register_blueprints(app):
        from user.views import user
        from payments.views import payment_bp

        app.register_blueprint(user)
        app.register_blueprint(payment_bp)

    app = Flask(__name__)
    app.config.from_object(config[environment])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # app.jinja_env.filters['zip'] = zip

    init_dependencies(app)
    register_blueprints(app)
    login_manager.init_app(app)

    return app


# set FLASK_CONFIG to switch environment;
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.before_first_request
def set_session_as_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)


@user_logged_in.connect_via(app)
def _after_login_hook(sender, user, **extra):
    try:
        user.update_last_login()
    except AttributeError:
        pass


@user_logged_out.connect_via(app)
def _after_logout_hook(sender, user, **extra):
    try:
        user.update_logout()
    except AttributeError:
        pass


def before_user_blueprint():
    from flask import request, current_app, redirect, url_for
    if request.path == current_app.config["USER_LOGIN_URL"]:
        return redirect(url_for("user.custom_login"))
    # if request.path == current_app.config["USER_REGISTER_URL"]:
    #     return redirect(url_for("user.onboard"))


app.before_request_funcs = {
    # blueprint name: [list_of_functions]
    'user': [before_user_blueprint, ]
}
