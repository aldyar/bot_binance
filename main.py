import asyncio
from aiogram import Dispatcher, Bot
from config import TOKEN
from handlers import router
import sys


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())