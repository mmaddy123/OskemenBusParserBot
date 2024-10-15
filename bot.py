import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.methods import DeleteWebhook
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares import AllowedUsersMiddleware

load_dotenv()

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

bot = Bot(token=os.getenv("BOT_TOKEN"),
          default=DefaultBotProperties(parse_mode='HTML'))


async def main():
    from handlers import common, incoming_bus

    dp.include_router(common.common)
    dp.include_router(incoming_bus.buses)

    dp.update.middleware(AllowedUsersMiddleware())

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
