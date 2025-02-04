from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


common = Router()


HELP_TEXT = """
/start - используйте эту команду для запуска бота
/get_incoming_bus - используйте эту команду для прибывающего автобуса
/cancel - используйте эту команду для отмены действия
<b>Ботом можно пользоваться по рабочему графику автобусов!</b>
"""


@common.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name}")


@common.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup=ReplyKeyboardRemove())


@common.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(text=HELP_TEXT)
