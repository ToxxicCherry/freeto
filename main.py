import asyncio
from telegram.handlers import *
from telegram import bot, dp
from db import init_db

async def main():
    await init_db()
    await dp.start_polling(bot, skip_updates=False)

if __name__ == '__main__':
    asyncio.run(main())