from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states import BusStop
from keyboards import create_bus_routes_buttons
from parsers import OskemenBusParser
from parsers.oskemen_bus_parser import get_bus_stop_names
from middlewares import BusParserMiddleWare


buses = Router()
buses.message.middleware(BusParserMiddleWare(OskemenBusParser()))


@buses.message(Command("get_incoming_bus"))
async def get_incoming_bus_handler(message: types.Message, state: FSMContext):
    await message.answer("Введите название остановки: ")
    await state.set_state(BusStop.bus_stop_name)


@buses.message(BusStop.bus_stop_name, F.text.in_(get_bus_stop_names().keys()))
async def select_bus_stop_handler(message: types.Message, state: FSMContext, bus_parser: OskemenBusParser):
    bus_parser.bus_stop_name = message.text
    bus_parser.get_bus_stop_json()
    await message.answer("Ищем доступные маршруты...")
    bus_routes = bus_parser.get_bus_routes()

    if bus_routes is None:
        await message.answer(text="По данной остановке не найдено транспортных средств")
        await state.clear()
    else:
        bus_routes_keyboard = create_bus_routes_buttons(bus_routes)
        await message.answer(text="Выберите нужный маршрут", reply_markup=bus_routes_keyboard)
        await state.set_state(BusStop.bus_route)


@buses.message(BusStop.bus_stop_name)
async def selected_incorrect_bus_stop_handler(message: types.Message):
    await message.answer("Остановки с таким названием не существует")
    await message.answer("Введите название остановки еще раз или посмотрите список доступных"
                         "автобусных остановок через команду /get_bus_stops")


@buses.message(BusStop.bus_route)
async def select_bus_route_handler(message: types.Message, state: FSMContext, bus_parser: OskemenBusParser):
    bus_parser.bus_route = message.text
    incoming_bus = bus_parser.get_incoming_bus()
    if incoming_bus is not None:
        result = f"🚏 Остановка: {bus_parser.bus_stop_name}\n" \
                 f"🚍 Маршрут: {bus_parser.bus_route}\n" \
                 f"⌛️ Прибудет через: {incoming_bus[0]}\n"\
                 f"⌛️ Следующий прибудет через: {incoming_bus[1]}\n"
        await message.answer_location(latitude=incoming_bus[2],
                                      longitude=incoming_bus[3])
        await message.answer(text=result, reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text="Автобусы пока остановили движение")
    await state.clear()

# @router.message(SelectBusStop.bus_route)
# async def selected_incorrect_bus_route(message: types.Message):
#     await message.answer("Такого маршрута нет или автобусы на данный момент не ходят\n"
#                          "Выберите другой маршрут или отмените действие командой /cancel: ")
