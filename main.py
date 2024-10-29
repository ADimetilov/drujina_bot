import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
import config
import handlers

async def main():
    try:
         # в proxy указан прокси сервер pythonanywhere, он нужен для подключения
        bot = Bot(token = config.BOT_TOKEN,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp = Dispatcher(storage = MemoryStorage())
        dp.include_router(handlers.router)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot,allowed_updates=dp.resolve_used_update_types())
    except Exception as error:
        print("Произошла ошибка",str(error))
        await asyncio.run(main())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())