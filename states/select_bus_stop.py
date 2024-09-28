from aiogram.filters.state import StatesGroup, State


class SelectBusStop(StatesGroup):
    bus_stop_name = State()
    bus_stop_html = State()
    bus_route = State()

