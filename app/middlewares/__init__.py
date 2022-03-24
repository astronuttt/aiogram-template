import os

from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from app.middlewares.acl import ACLMiddleware
from app.middlewares.throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    """setup middlewares
    example:
    dp.middleware.setup(Middleware())
    """
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(ACLMiddleware())
    if os.getenv("LOG_LEVEL", None) == "debug":
        dp.middleware.setup(LoggingMiddleware())
