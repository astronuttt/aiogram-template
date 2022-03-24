from typing import Any, Dict, List

from aiogram import types
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.main import log
from app.models.user import User
from app.utils.context import current_user
from app.utils.typing import extract_vars_from_callback_data


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: Dict, user: types.User, message: types.Message):
        user = (await User.get_or_create(id=user.id))[0]
        data["user"] = user

    async def set_user(self, data: Dict[str, Any]):
        """
        set user in current_user contextvar, for using it later in filters and ...
        """
        user: User = data.get("user", None)
        ctx_token = current_user.set(user)
        log.debug(f"setting up user with {user=} and {ctx_token=}")
        data["ctx_token"] = ctx_token

    async def reset_user(self, data: Dict[str, Any]):
        """
        reset user in current_user contextvar
        """
        user, ctx_token = data["user"], data["ctx_token"]
        log.debug(f"resettingl user with {user=} and {ctx_token=}")
        current_user.reset(ctx_token)

    async def setup_callback_query_data(
        self, data: Dict, user: types.User, query: types.CallbackQuery
    ):
        """setup query data
        you can define variables in callback data and arguments
                    for a handler like: order_id: int and
        it will be extracted from the callback_data and will be
                passed to the function as that argument
        callback_data format: ikb:getorders:order_id=5
        each variable needs to be seperated with ":" and must start with "ikb"
        """
        handler = current_handler.get()
        query_data = query.data.split(":")
        query_vars = extract_vars_from_callback_data(query_data, handler)
        data.update(query_vars)

    async def on_pre_process_message(self, message: types.Message, data: Dict):
        await self.setup_chat(data, message.from_user, message)
        await self.set_user(data)

    async def on_pre_process_callback_query(
        self, query: types.CallbackQuery, data: Dict
    ):
        await self.setup_chat(data, query.from_user, query.message)
        await self.set_user(data)

    async def on_process_callback_query(self, query: types.CallbackQuery, data: Dict):
        await self.setup_callback_query_data(data, query.from_user, query)

    async def on_post_process_message(
        self, message: types.Message, results: List[Any], data: Dict[str, Any]
    ):
        await self.reset_user(data)

    async def on_post_process_callback_query(
        self, query: types.CallbackQuery, results: List[Any], data: Dict[str, Any]
    ):
        await self.reset_user(data)
