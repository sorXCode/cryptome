from dotenv import load_dotenv
# load envrionment variables from '.env' file
load_dotenv()

import os
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel
from config import config
from flask_user import UserManager
from coinbase_commerce.client import Client

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "/"
babel = Babel()
coinbase_client = Client(os.environ["COINBASE_APIKEY"])


def create_app(environment):
    def init_dependencies(app):
        from user import models

        db.init_app(app)
        login_manager.init_app(app)
        babel.init_app(app)
        UserManager(app, db, models.User)
    
    def register_blueprints(app):
        from user.views import user_bp
        from payments.views import payment_bp

        app.register_blueprint(user_bp)
        app.register_blueprint(payment_bp)

    app = Flask(__name__)
    app.config.from_object(config[environment])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # app.jinja_env.filters['zip'] = zip
    
    init_dependencies(app)
    register_blueprints(app)
    
    return app

#set FLASK_CONFIG to switch environment;
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
