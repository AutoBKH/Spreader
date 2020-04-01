import logging
import os

JSON_FORMATTER = logging.Formatter(
    """{
    "time": "%(asctime)s",
    "name": "%(name)s",
    "level": "%(levelname)s",
    "message": "%(message)s"
}""")

# TODO: take BASE_PATH from config which depends on environment variable (prod, dev, etc...)
LOGGER_BASE_PATH = r'logs'


def get_logger(name, min_level=logging.INFO, formatter=JSON_FORMATTER):
    logger = logging.getLogger(name)
    logger_handler = logging.FileHandler(LOGGER_BASE_PATH + os.path.sep + name)
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.setLevel(min_level)
    return logger
