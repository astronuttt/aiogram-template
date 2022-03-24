import aioredis
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import Executor

from app import config

from .logger import get_logger

log = get_logger(__name__)


fsm_storage = RedisStorage2(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_FSM_DB,
)


async def get_redis_pool() -> aioredis.Redis:
    """create redis pool"""
    return await aioredis.from_url(
        f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}",
        db=config.REDIS_DB,
        encoding="utf-8",
        decode_responses=True,
    )


bot = Bot(token=config.TELEGRAM_TOKEN, proxy=config.PROXY, parse_mode=config.PARSE_MODE)
dp = Dispatcher(bot=bot, storage=fsm_storage)
executor = Executor(dispatcher=dp, skip_updates=True, check_ip=True)
redis = executor.loop.run_until_complete(get_redis_pool())


async def on_webhook_startup(dispatcher: Dispatcher):
    """will run on webhook startup"""
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_webhook_shutdown(dispatcher: Dispatcher):
    """will run on webhook shutdown"""
    log.info("Deleting webhook...")
    await bot.delete_webhook()
    log.info("Telegram webhook was deleted.")

    # close DB connections
    await redis.close()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def on_polling_startup(dispatcher: Dispatcher):
    """will run on polling startup"""


async def on_polling_shutdown(dispatcher: Dispatcher):
    """will run on polling shutdown"""

    # close DB connections
    await redis.close()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def start():
    """setup the parts for application to start"""
    from app import filters, middlewares
    from app.models import database

    database.setup(executor)
    middlewares.setup(dp)
    filters.setup(dp)

    import app.handlers  # noqa

    if config.MODE == "webhook":
        executor.on_startup(on_webhook_startup)
        executor.on_shutdown(on_webhook_shutdown)
        executor.start_webhook(
            config.WEBHOOK_PATH,
            host=config.WEBAPP_HOST,
            port=config.WEBAPP_PORT,
        )
    elif config.MODE == "polling":
        executor.on_startup(on_polling_startup)
        executor.on_shutdown(on_polling_shutdown)
        executor.start_polling()
    else:
        log.error(
            f"Unknown mode: '{config.MODE}'! it should be 'webhook' or 'polling'."
        )
