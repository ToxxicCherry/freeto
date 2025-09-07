from aiogram.filters import Command
from aiogram.types import Message
from .cruds import create_user
from .bot import bot, dp
from .keyboards import main_menu_kb


@dp.message(Command('start'))
async def start_command(message: Message):
    await create_user(
        tg_id=str(message.from_user.id),
        username=message.from_user.username,
    )

    await bot.send_message(
        message.chat.id,
        text='КРЯ!',
        reply_markup=main_menu_kb
    )