import os
import sys
from flask_api import FlaskAPI
from log import log
from config import app_config

config_name: str = os.getenv("APP_SETTINGS")

if config_name is None:
    log.error("Missing APP_SETTINGS= environment variable.")
    sys.exit(0)


def create_app() -> FlaskAPI:

    app: FlaskAPI = FlaskAPI(__name__)
    app.config.from_object(app_config[config_name])
    app.config['ENV'] = config_name
    return app


app = create_app()


if __name__ == '__main__':
    from trades import setup_kraken_websocket
    setup_kraken_websocket()
