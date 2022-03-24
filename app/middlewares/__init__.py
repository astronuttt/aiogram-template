import os
from aiogram import Dispatcher

from app.middlewares.throttling import ThrottlingMiddleware
from app.middlewares.acl import ACLMiddleware
from aiogram.contrib.middlewares.logging import LoggingMiddleware


def setup(dp: Dispatcher):
    """setup middlewares
    example:
    dp.middleware.setup(Middleware())
    """
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(ACLMiddleware())
    if os.getenv("LOG_LEVEL", None) == "debug":
        dp.middleware.setup(LoggingMiddleware())
