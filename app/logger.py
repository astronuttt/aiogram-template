import os
import logging


def get_logger(name: str) -> logging.Logger:
    formatter = logging.Formatter(fmt="%(levelname)s:%(name)s:%(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(os.getenv("LOG_LEVEL", "info").upper())
    logger.addHandler(handler)
    logger.propagate = False
    return logger
