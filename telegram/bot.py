from config import settings
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=settings.bot_token)
dp = Dispatcher(storage=MemoryStorage())
