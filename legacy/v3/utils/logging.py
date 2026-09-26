from logging import getLogger, StreamHandler, Formatter, INFO
import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = StreamHandler()
    formatter = Formatter("%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    return logger