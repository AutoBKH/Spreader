import logging
import os

FORMATTER = logging.Formatter('[%(levelname)s] - %(asctime)s - %(name)s - %(message)s')
# TODO: take BASE_PATH from config which depends on environment variable (prod, dev, etc...)
LOGGER_BASE_PATH = r'C:\Users\Shani Hochma\PycharmProjects\ShaniIsWorking\logs'


def get_logger(name, min_level=logging.INFO, formatter=FORMATTER):
    logger = logging.getLogger(name)
    logger_handler = logging.FileHandler(LOGGER_BASE_PATH + os.path.sep + name)
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.setLevel(min_level)
    return logger
