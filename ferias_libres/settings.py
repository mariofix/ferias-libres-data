import logging.config
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "change-me"
DEBUG = True
LOG_LEVEL = "INFO"
ALLOWED_DOMAINS = ["tardis.local", "127.0.0.1"]
SQLALCHEMY_DATABASE_URI = "sqlite:///app.sqlite3"
SQLALCHEMY_RECORD_QUERIES = DEBUG
SQLALCHEMY_ECHO = False
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 1800}

FLASK_ADMIN_SWATCH = "yeti"
FLASK_ADMIN_FLUID_LAYOUT = True

# Flask-Security config
SECURITY_URL_PREFIX = "/security/"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"

SECURITY_POST_LOGIN_VIEW = "/admin.site/"
SECURITY_POST_LOGOUT_VIEW = "/login/"

# Flask-Security features
SECURITY_REGISTERABLE = False
SECURITY_TRACKABLE = True
SECURITY_USERNAME_ENABLE = True

# Flask-Babel
BABEL_DEFAULT_LOCALE = "en"
BABEL_DEFAULT_TIMEZONE = "America/Santiago"
BABEL_DEFAULT_FOLDER = "firenze/translations"
LANGUAGES = {
    "en": {"flag": "en", "name": "English"},
    "es": {"flag": "cl", "name": "Español"},
}

# Debug-Toolbar
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG_TB_PROFILER_ENABLED = False


# Flask-Mail
# MAIL_SERVER = "localhost"
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USERNAME = ""
# MAIL_PASSWORD = ""
# MAIL_TIMEOUT = 5
# MAIL_DEFAULT_SENDER = "tests@mariofix.com"
# MAIL_USE_LOCALTIME = True

# Celery
# CELERY_BROKER_URL = "redis://172.16.17.2:6379/10"
# CELERY_LOG_LEVEL = "DEBUG" if DEBUG else LOG_LEVEL
# CELERY_SCHEDULER = False

APP_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname}:\t  {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{asctime} {name}.{levelname} {filename}({lineno}) {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG" if DEBUG else LOG_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/api.log",
            "formatter": "verbose",
            "when": "midnight",
            "interval": 1,
        },
        "console": {
            "level": "DEBUG" if DEBUG else LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["file", "console"],
        },
    },
}
