import sys
import os
import json
from pathlib import Path
from uuid import uuid4

from dateutil import tz

from log import log

PAIRS_TO_WATCH = ["XBT/EUR", "XLM/EUR", "ETH/EUR", "XRP/EUR"]

API_KEYS = {
    "trade": uuid4(),
}

TZ_UTC = tz.gettz('UTC')
TZ_AMS = tz.gettz('Europe/Amsterdam')


def setup_app() -> str:
    try:
        return os.environ["APP_SETTINGS"]
    except KeyError:
        print("No APP_SETTINGS environment variable.")
        sys.exit()


MODE = setup_app()


def get_db_config(filename=None):
    home = str(Path.home())

    if filename is None:
        filename = f"{home}/.kraken/db_settings.conf"
        log.warning(f"No database credential file given. Trying: {filename}")

    try:
        with open(filename, "r") as fp:
            settings = json.load(fp)
    except Exception as e:
        log.error(f"Could not open database credentials: {filename}")
        log.error(e)
        sys.exit(1)

    if settings:
        return settings


class Config(object):
    db_config = get_db_config()

    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    DB_TYPE = db_config["type"]
    DB_USER = db_config["user"]
    DB_PASS = db_config["password"]
    DB_HOST = db_config["host"]
    DB_NAME = db_config["db_name"]
    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
