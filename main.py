import asyncio
from aiogram import Dispatcher, Bot
from config import TOKEN
from handlers import router
import sys
from database.models import async_main

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

async def on_startup(dispatcher):
    await async_main()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass