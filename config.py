from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config(object):
    DEBUG = True
    TESTING = True
    DEVELOPMENT = True

    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_DATABASE_URI = (
        environ["DATABASE_URL"] if "DATABASE_URL" in environ else "DATABASE_URL env variable is missing"
    )
    API_KEY = environ["API_KEY"] if "API_KEY" in environ else "API_KEY env variable is missing"

    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"

    SECURITY_POST_LOGIN_VIEW = "/admin/story/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
