import sys
from websocket import Client
from db import db
from db.models import Trades
from log import log


def trade_handler(data):

    session = db.session()
    pair = data[3]

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


trade_client = Client(
    channel_name="trade",
    pairs=["XBT/EUR"],
    subscription_args={"name":"trade"}
)

log.info(f"Starting trade collection...")
trade_client.websocket.start()
