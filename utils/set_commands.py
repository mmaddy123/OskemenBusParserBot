from aiogram.types import BotCommand
from aiogram import Bot


async def setup_bot_commands(bot: Bot):
    bot_commands = [
        BotCommand(command='/start', description="Запустить бота"),
        BotCommand(command='/get_incoming_bus', description="Узнать время подъезжающего автобуса")
    ]
    await bot.set_my_commands(bot_commands)
