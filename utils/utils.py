import logging

FORMATTER = logging.Formatter('[%(levelname)s] - %(asctime)s - %(name)s - %(message)s')


def get_logger(name, path, min_level=logging.INFO, formatter=FORMATTER):
    logger = logging.getLogger(name)
    logger_handler = logging.FileHandler(path)
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.setLevel(min_level)
    return logger
