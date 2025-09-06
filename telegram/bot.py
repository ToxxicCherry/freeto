from config import settings
from aiogram import Bot, Dispatcher

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
