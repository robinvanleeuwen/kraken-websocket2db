import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter


STREAM_FORMAT = "%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
FILE_FORMAT = "%(log_color)s %(asctime)s %(levelname)s %(funcName)s(%(lineno)d) | %(log_color)s %(message)s"
LOG_FILE = "/var/log/kraken-trades.log"
LOG_LEVEL = logging.DEBUG

logging.root.setLevel(LOG_LEVEL)

ColoredFormatter(STREAM_FORMAT)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(LOG_LEVEL)
stream_handler.setFormatter(ColoredFormatter(STREAM_FORMAT))

file_handler = RotatingFileHandler(LOG_FILE, mode="a", maxBytes=5 * 1024 * 1024, backupCount=2, encoding=None, delay=0)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(ColoredFormatter(FILE_FORMAT))
log = logging.getLogger("pythonConfig")

log.setLevel(LOG_LEVEL)
log.addHandler(stream_handler)
log.addHandler(file_handler)