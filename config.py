import sys
import os
from dateutil import tz

PAIRS_TO_WATCH = ["XBT/EUR", "XLM/EUR", "ETH/EUR", "XRP/EUR"]

TZ_UTC = tz.gettz('UTC')
TZ_AMS = tz.gettz('Europe/Amsterdam')

def setup_app() -> str:
    try:
        return os.environ["APP_SETTINGS"]
    except KeyError:
        print("No APP_SETTINGS environment variable.")
        sys.exit()

MODE = setup_app()

def get_db_credentials(filename=None):
    if filename is None:
        filename = "/home/rvl/.kraken/postgresql"
    fp = open(filename, "r")
    lines = fp.readlines()
    for l in lines:
        creds = l.split(":")
        creds[1] = creds[1].rstrip()
        return creds


class Config(object):


    db_credentials = get_db_credentials()

    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    DB_USER = str(db_credentials[0])
    DB_PASS = str(db_credentials[1])
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@htpc/aws"
    SQLALCHEMY_TRACK_MODIFICATIONS=False

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
