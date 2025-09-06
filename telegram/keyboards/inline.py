from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_inline_keyboard(options: list[str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=option, callback_data=option)] for option in options
        ]
    )