from tortoise import Tortoise
from tortoise.fields import DatetimeField
from tortoise.models import Model
from aiogram import Dispatcher
from aiogram.utils.executor import Executor

from app import config


db = Tortoise()


class Base(Model):
    class Meta:
        abstract = True


class TimedBase(Base):
    class Meta:
        abstract = True

    created_at = DatetimeField(null=True, auto_now_add=True)
    updated_at = DatetimeField(null=True, auto_now=True)


async def on_startup(dispatcher: Dispatcher):
    await db.init(config=config.TORTOISE_ORM)


async def on_shutdown(dispatcher: Dispatcher):
    await db.close_connections()


def setup(executor: Executor):
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
