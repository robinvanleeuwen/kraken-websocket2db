from log import log
from singleton import Singleton
from websocket import Client


class OrderBook(metaclass=Singleton):

    def __init__(self):

        self.book = dict()

    def create(self, data):
        pair = data[-1]
        self.book[pair] = dict()
        self.book[pair]["ask"] = dict()
        self.book[pair]["bid"] = dict()
        for item in data[1]["as"]:
            self.book[pair]["ask"][item[0]] = [item[1], item[2]]
        for item in data[1]["bs"]:
            self.book[pair]["bid"][item[0]] = [item[1], item[2]]

    def update(self, data: list):
        pair = data[-1]

        if "a" in data[1].keys():
            book_type = "ask"

        elif "b" in data[1].keys():
            book_type = "bid"

        for item in data[1][book_type[0]]:
            if item[1] == '0.00000000' and item[0] in self.book[pair][book_type].keys():
                del self.book[pair][book_type][item[0]]
            else:
                self.book[pair][book_type][item[0]] = [item[1], item[2]]


order_book = OrderBook()


def book_handler(data):

    if "as" in data[1].keys() or "bs" in data[1].keys():
        order_book.create(data)
    else:
        order_book.update(data)


book_client = Client(
    channel_name="book",
    pairs=["XBT/EUR"],
    subscription_args={"name":"book", "depth": 1000}
)

log.info(f"Starting book collection...")
book_client.websocket.start()