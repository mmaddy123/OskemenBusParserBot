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


# @router.message()
# async def echo(message: types.Message):
#     await message.answer("Я вас не понял")


# start_handler.py
# from aiogram import types
# from aiogram.filters.command import Command
# from bot import dp
#
#
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer(f"Hello {message.from_user.username}")


# echo_handler.py
# from aiogram import types
# from bot import dp
#
#
# @dp.message()
# async def echo(message: types.Message):
#     await message.answer("Я вас не понял")

# cancel_handler.py
# from aiogram import types
# from aiogram.types import ReplyKeyboardRemove
# from aiogram.filters.command import Command
# from aiogram.fsm.context import FSMContext
# from bot import dp
#
#
# @dp.message(Command("/cancel"))
# async def cmd_cancel(message: types.Message, state: FSMContext):
#     await state.clear()
#     await message.answer(text="Действие отменено", reply_markup=ReplyKeyboardRemove())



