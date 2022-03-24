from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.main import log, redis

THROTTLING_COUNT = "throttling_count"
THROTTLING_DURATION = "throttling_duration"
THROTTLING_LIMIT_FOR = "throttling_limit_for"
THROTTLING_KEY = "throttling_key"
THROTTLING_MESSAGE = "throttling_message"
DEFAULT_THROTTLE_MESSAGE = "Too many requests! please retry in {limit_for} seconds."


def rate_limit(
    count: int = 5,
    duration: int = 10,
    limit_for: int = 30,
    key: str = "default",
    message: str = DEFAULT_THROTTLE_MESSAGE,
):
    """
    Decorator for configuring rate limit and key in different functions.
    :param count: how many messages
    :param duration: in what duration of time
    :param limit_for: how many seconds user be limited after throtteling
    :param key: to set different count/duration/limit_for for each function differently
    :return: callable
    """

    def decorator(func: callable):
        setattr(func, THROTTLING_COUNT, count)
        setattr(func, THROTTLING_DURATION, duration)
        setattr(func, THROTTLING_LIMIT_FOR, limit_for)
        setattr(func, THROTTLING_KEY, key)
        setattr(func, THROTTLING_MESSAGE, message)
        setattr(func, "has_limit", True)
        log.debug(
            f"setting up rate_limits for '{func.__name__}': "
            f"{count=}, {duration=}, {limit_for=}, {key=}"
        )
        return func

    return decorator


async def set_throttle(
    msg: types.Message, count: int, duration: int, limit_for: int, key: str
):
    USER_FLOOD_KEY = f"user_flood:{key}:{msg.from_user.id}"

    bucket = await redis.get(USER_FLOOD_KEY)

    if bucket is None:
        await redis.setex(USER_FLOOD_KEY, duration, 1)
        bucket = 1
    else:
        await redis.incrby(USER_FLOOD_KEY, 1)

    # Calculate
    if (int(bucket) + 1) >= count:
        await redis.setex(f"user_limited:{key}:{msg.from_user.id}", limit_for, "True")
        # raise Throttled(count=count, duration=duration, limit_for=limit_for, key=key)


async def check_throttled(
    msg: types.Message,
    throttle_key: str = "default",
    throttle_message: str = DEFAULT_THROTTLE_MESSAGE,
):
    if await redis.exists(f"user_limited:{throttle_key}:{msg.from_user.id}"):
        limit_for = await redis.ttl(f"user_limited:{throttle_key}:{msg.from_user.id}")
        await msg.reply(text=throttle_message.format(limit_for=limit_for))
        raise CancelHandler()


class ThrottlingMiddleware(BaseMiddleware):
    """
    Thorrettling middleware to prevent request spam from a user
    """

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message
        :param message:
        """
        # Get current handler
        handler = current_handler.get()
        is_limited_handler = getattr(handler, "has_limit", False)

        # If handler was configured, get rate limit and key from handler
        if is_limited_handler:
            key = getattr(handler, THROTTLING_KEY, "default")
            throttle_message = getattr(handler, THROTTLING_MESSAGE)
            count = getattr(handler, THROTTLING_COUNT)
            duration = getattr(handler, THROTTLING_DURATION)
            limit_for = getattr(handler, THROTTLING_LIMIT_FOR)

            await check_throttled(message, key, throttle_message)

            await set_throttle(message, count, duration, limit_for, key)
