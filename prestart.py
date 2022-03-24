import logging
import asyncio
import subprocess

from tenacity import (
    after_log,
    before_log,
    retry,
    stop_after_attempt,
    wait_fixed,
)

from tortoise import Tortoise
from app.api import Addino, Request
from app import config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def db_pre_init():
    try:
        db = Tortoise()
        await db.init(config=config.TORTOISE_ORM)
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        await db.close_connections()


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def api_pre_init():
    try:
        api = Addino(Request())
        result = await api.status()
        if result.status == "online":
            logger.info("API status check: ok")
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        await api.request.session.close()


def main() -> None:
    loop = asyncio.get_event_loop()
    logger.info("Initializing service: DB")
    loop.run_until_complete(db_pre_init())
    logger.info("Initializing service: api")
    loop.run_until_complete(api_pre_init())
    logger.info("Services finished initializing")

    logger.info("Initializing migration")
    subprocess.run(["aerich", "upgrade"])
    logger.info("Migration finished")


if __name__ == "__main__":
    main()
