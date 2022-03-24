from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters.filters import BoundFilter

from app.utils.context import current_user


@dataclass
class IsSuperUser(BoundFilter):
    key = "super_user"
    super_user: bool

    async def check(self, message: types.Message) -> bool:
        return current_user.super_user


@dataclass
class CallbackDataPrefix(BoundFilter):
    key = "callback_data_prefix"
    callback_data_prefix: str

    async def check(self, query: types.CallbackQuery) -> bool:
        if query.data.startswith(self.callback_data_prefix):
            return True
        return False
