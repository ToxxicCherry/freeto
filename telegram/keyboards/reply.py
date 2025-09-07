from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Найти код")],
        [KeyboardButton(text="Ввести код")]
    ], resize_keyboard=True
)