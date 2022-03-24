from aiogram.dispatcher.filters.state import State, StatesGroup


class LoginForm(StatesGroup):
    phone_number = State()
    code = State()


class OrderForm(StatesGroup):
    service = State()
    count = State()
    viewcount = State()
    chat_id = State()
    fromgroup_chat_id = State()


class ChargeAccountForm(StatesGroup):
    amount = State()
