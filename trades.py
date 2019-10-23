import os
import sys

from kraken_wsclient_py import kraken_wsclient_py as kraken_client
from config import PAIRS_TO_WATCH, API_KEYS
from db import db
from db.models import Trades, ActiveAPI
from log import log


def register_api_handler(api_name: str):

    try:
        api_key = API_KEYS[api_name]
    except KeyError:
        log.error(f"Could not find valid api_key for registering '{api_name}'-api")
        client.stop()

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


def handle_data(data):

    if type(data) is dict:
        pass

    if type(data) is list:
        channel_id = data[0]
        channel_name = data[2]
        pair = data[3]

        session = db.session()

        if channel_name == "trade":

            if not valid_api_key(api_name="trade"):
                client.stop()

            for d in data[1]:
                record = Trades()
                record.pair = pair
                record.price = float(d[0])
                record.volume = float(d[1])
                record.time = float(d[2])
                record.side = str(d[3])
                record.order_type = str(d[4])
                record.misc = str(d[5])
                session.add(record)
            try:
                session.commit()
                print("↓", end="")
                sys.stdout.flush()
            except Exception as e:
                print(e)


def setup_kraken_websocket():
    pass
log.info("Creating Kraken Websocket Client")
client = kraken_client.WssClient()

# Setup trades
log.info(f"Subscribing to trade channel for pairs: { PAIRS_TO_WATCH }")
client.subscribe_public(
    subscription={
        "name": "trade",
    },
    pair=PAIRS_TO_WATCH,
    callback=handle_data
)
log.info("Starting collection of trades...")
register_api_handler("trade")
client.start()


