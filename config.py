import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Production:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = bool(os.environ.get("DEBUG", False))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'production_db.sqlite')

class Development:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_REFRESH_EACH_REQUEST = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'development_db.sqlite')
    # Flask-User settings
    USER_APP_NAME = "Cryptome"      # Shown in and email templates and page footers
    USER_APP_EMAIL = "Cryptome"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form
    USER_LOGIN_URL = '/signin'
    USER_LOGOUT_URL = '/logout'
    USER_REGISTER_URL = '/register'
    USER_ENABLE_INVITE_USER = True
    USER_ENABLE_EMAIL = True
    MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']
    USER_EMAIL_SENDER_EMAIL = os.environ['MAIL_DEFAULT_SENDER']
    SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]



class Test:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    TESTING = True
    WTF_CSRF_ENABLED = False
    SERVER_NAME = '127.0.0.1:5000'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test_db.sqlite')

    # Flask-User settings
    USER_APP_NAME = "Cryptome"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form

config = {
    'development': Development,
    'test': Test,
    'default': Development
}