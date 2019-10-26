import os, sys

from kraken_wsclient_py import kraken_wsclient_py as kraken_client
from config import PAIRS_TO_WATCH, API_KEYS
from db.models import ActiveAPI
from db import db
from log import log


class Client:

    def __init__(self, channel_name: str, pairs: list, subscription_args: dict):
        log.info("Creating Kraken Websocket Client")

        self.register_api_handler(channel_name)
        self.websocket = kraken_client.WssClient()


        # Setup trades
        log.info(f"Subscribing to {channel_name} channel for pairs: {PAIRS_TO_WATCH}")

        self.websocket.subscribe_public(
            subscription=subscription_args,
            pair=PAIRS_TO_WATCH,
            callback=self.handler
        )

    @staticmethod
    def valid_api_key(api_name: str) -> bool:

        try:
            api_key = API_KEYS[api_name].__str__()
        except KeyError:
            log.error(f"Could not find valid api_key for registering '{api_name}'-api")
            sys.exit(0)

        session = db.session()
        active_api = session.query(ActiveAPI).filter(ActiveAPI.api_name == api_name).one_or_none()
        if active_api is None:
            log.error(f"Failure retrieving active API key from database for {api_name}")
            return False

        elif active_api.api_key != api_key:
            log.error(f"No valid API key for '{api_name}' (probably replaced by another websocket thread)")
            return False

        return True

    def register_api_handler(self, api_name: str):

        try:
            api_key = API_KEYS[api_name]
        except KeyError:
            log.error(f"Could not find valid api_key for registering '{api_name}'-api")
            self.websocket.stop()

        log.info(f"Registering '{api_name}'-API with key: {api_key} ")
        session = db.session()
        record = ActiveAPI()
        record.api_key = api_key
        record.api_name = api_name
        session.merge(record)
        try:
            session.commit()
        except Exception as e:
            print(e)
            os.exit(1)

    def handler(self, data):

        if type(data) is dict:
            pass

        if type(data) is list:

            channel_name = data[-2]

            if channel_name == "trade":

                if not self.valid_api_key(api_name="trade"):
                    self.websocket.stop()

                from trades import trade_handler
                trade_handler(data)

            elif "book-" in channel_name:

                if not self.valid_api_key(api_name="book"):
                    self.websocket.stop()

                from book import book_handler
                book_handler(data)
            else:
                log.warning("Could not determine channel")
                log.debug(data)


