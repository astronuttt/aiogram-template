#!/usr/bin/env python3

import os

from functools import wraps
import argparse
import logging
from app.logger import get_logger


log = get_logger(__name__)


try:
    import aiohttp_autoreload

    auto_reload_available = True
except ImportError:
    auto_reload_available = None


parser = argparse.ArgumentParser(description="Aiogram executor")
parser.add_argument(
    "--reload",
    "-r",
    required=False,
    action="store_true",
    help="run the Application in auto-reload mode"
    "(aiohttp_autoreload need to be installed)",
)
parser.add_argument(
    "--debug",
    "-d",
    required=False,
    action="store_true",
    help="run application in debug mode",
)


args = parser.parse_args()


def arg_parser_mixin(func):
    auto_reload = args.reload
    debug = args.debug

    @wraps(func)
    def wrapper(*args, **kwargs):
        if (log_level := os.getenv("LOG_LEVEL", None)) is not None:
            log.info(f"Setting Log level to {log_level}")
            logging.basicConfig(level=logging.getLevelName(log_level.upper()))

        if debug:
            logging.basicConfig(level=logging.DEBUG)
            os.environ["LOG_LEVEL"] = "debug"
        else:
            logging.basicConfig(level=logging.INFO)

        if auto_reload_available and auto_reload:
            log.warning(
                "Application started in auto-reload mode. "
                "make sure to disable it in production server!"
            )
            aiohttp_autoreload.start()
        elif auto_reload and not auto_reload_available:
            log.error(
                "auto-reload is enabled but 'aiohttp_autoreload' "
                "is not installed! skipping..."
            )

        func(*args, **kwargs)

    return wrapper


@arg_parser_mixin
def start_app():
    """start app and start aiohttp_autoreload for auto-reload
    if aiohttp_autoreload installed and auto_reload enabled
    """
    log.info("Starting application...")
    from app.main import start

    start()


if __name__ == "__main__":
    start_app()
