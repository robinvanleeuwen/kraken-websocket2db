from kraken_wsclient_py import kraken_wsclient_py as kraken_client
from config import MODE, PAIRS_TO_WATCH, TZ_AMS, TZ_UTC, app_config
from db import db
from db.models import Trades
from log import log


def handle_data(data):

    if type(data) is dict:
        pass

    if type(data) is list:
        channel_id = data[0]
        channel_name = data[2]
        pair = data[3]

        session = db.session()

        if channel_name == "trade":
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
                session.commit()


def setup_kraken_websocket():
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
    client.start()
