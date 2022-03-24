from abc import ABC, abstractmethod
from typing import List, Dict
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class RegularKeyboard(ABC):

    # global keyboards
    # list of all keywords for cancel in subclasses
    cancel_list = []

    @classmethod
    @abstractmethod
    def get(*args, **kwargs) -> ReplyKeyboardMarkup:
        pass

    @staticmethod
    def _create_multiple(
        multiple_keys: List[str], row_width: int = 3
    ) -> List[List[KeyboardButton]]:
        keys = list(map(KeyboardButton, multiple_keys))
        if len(keys) < 1 or row_width < 2:
            return keys
        # reverse the list so, the rows that are shorter that row_width come first
        return [keys[key : key + row_width] for key in range(0, len(keys), row_width)][
            ::-1
        ]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if hasattr(cls, "cancel"):
            cls.cancel_list.append(cls.cancel.text)


class InlineKeyboard(ABC):
    @classmethod
    @abstractmethod
    def get(*args, **kwargs) -> InlineKeyboardMarkup:
        pass

    def _create_multiple(
        multiple_keys: List[Dict[str, str]], row_width: int = 3
    ) -> List[List[InlineKeyboardButton]]:
        if len(multiple_keys) < 1:
            return []
        return [
            [
                InlineKeyboardButton(text=name, callback_data=cb)
                for name, cb in row.items()
            ]
            for row in multiple_keys
        ]
