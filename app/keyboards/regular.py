from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .base import RegularKeyboard


class MainMenuKeyboard(RegularKeyboard):
    @classmethod
    def get(cls) -> ReplyKeyboardMarkup:
        keyboard = [
            [KeyboardButton("let's start")],
        ]
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
