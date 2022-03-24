from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.keyboards.regular import MainMenuKeyboard
from app.main import dp, log
from app.models.user import User


@dp.message_handler(CommandStart(), state="*")
async def start(message: Message, user: User, state: FSMContext):
    if state and (current_state := await state.get_state()) is not None:
        log.debug(f"Canceling state: {current_state}")
        await state.finish()

    start_text = (
        "Welcome to the Bot!\n"
        "do you want me to get to know you better? "
        "press the let's start button bellow:"
    )
    return await message.answer(
        text=start_text,
        reply_markup=MainMenuKeyboard.get(),
    )
