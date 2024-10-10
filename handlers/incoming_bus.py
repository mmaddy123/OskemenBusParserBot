from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states import SelectBusStop
from oskemen_bus_parser import get_incoming_bus, get_bus_stop_names,\
    get_bus_routes, get_bus_stop_by_url, get_bus_stop_html
from keyboards import create_bus_routes_buttons


buses = Router()


@buses.message(Command("get_incoming_bus"))
async def get_incoming_bus_handler(message: types.Message, state: FSMContext):
    await message.answer("Введите название остановки: ")
    await state.set_state(SelectBusStop.bus_stop_name)


@buses.message(SelectBusStop.bus_stop_name, F.text.in_(get_bus_stop_names().keys()))
async def select_bus_stop_handler(message: types.Message, state: FSMContext):
    await state.update_data(bus_stop_name=message.text)
    await state.set_state(SelectBusStop.bus_stop_html)
    await message.answer("Ищем доступные маршруты...")
    await get_incoming_bus_html_handler(message, state)


@buses.message(SelectBusStop.bus_stop_name)
async def selected_incorrect_bus_stop_handler(message: types.Message):
    await message.answer("Остановки с таким названием не существует\n"
                         "Введите название остановки или посмотрите список доступных"
                         "автобусных остановок через команду /get_bus_stops")


@buses.message(SelectBusStop.bus_stop_html)
async def get_incoming_bus_html_handler(message: types.Message, state: FSMContext):
    bus_stop_data = await state.get_data()
    bus_stop_url = get_bus_stop_by_url(bus_stop_data["bus_stop_name"])
    bus_stop_html = get_bus_stop_html(bus_stop_url)
    await state.update_data(bus_stop_html=bus_stop_html)

    bus_routes = get_bus_routes(bus_stop_html)
    if bus_routes is None:
        await message.answer(text="По данной остановке не найдено транспортных средств")
        await state.clear()
    else:
        await message.answer(text="Выберите нужный маршрут", reply_markup=create_bus_routes_buttons(bus_routes))
        await state.set_state(SelectBusStop.bus_route)


@buses.message(SelectBusStop.bus_route)
async def select_bus_route_handler(message: types.Message, state: FSMContext):
    await state.update_data(bus_route=message.text)
    bus_route_data = await state.get_data()
    if get_bus_routes(bus_route_data["bus_stop_html"]) is None:
        await message.answer("По данной остановке не найдено транспортных средств")
        await state.clear()
    else:
        incoming_bus = get_incoming_bus(bus_route_data["bus_route"],
                                        bus_route_data["bus_stop_html"], bus_route_data["bus_stop_name"])
        result = f"🚏 Остановка: {incoming_bus[0]}\n" \
                 f"🚍 Маршрут: {incoming_bus[1]}\n" \
                 f"⌛️ Прибудет через: {incoming_bus[2]}\n"\
                 f"⌛️ Следующий прибудет через: {incoming_bus[3]}\n"
        await message.answer(text=result, reply_markup=ReplyKeyboardRemove())
        await state.clear()


# @router.message(SelectBusStop.bus_route)
# async def selected_incorrect_bus_route(message: types.Message):
#     await message.answer("Такого маршрута нет или автобусы на данный момент не ходят\n"
#                          "Выберите другой маршрут или отмените действие командой /cancel: ")



